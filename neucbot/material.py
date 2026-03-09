import os
import re

from bisect import bisect

from neucbot import elements
from neucbot import talys

N_A = 6.0221409e23
MeV_to_keV = 1.0e3
mb_to_cm2 = 1.0e-27

NEUTRON_CROSS_SECTION_PATTERN = re.compile(
    r"2. Binary non-elastic cross sections .non-exclusive.\n\n\s+gamma.*\n\s+neutron = (?P<cross_section>\d\.\d{5}E[\+\-]\d{2})"
)


class Isotope:
    # self.fraction should be a number between 0 and 1
    def __init__(self, element, mass_number, fraction):
        self.element = element
        self.mass_number = int(mass_number)
        self.fraction = float(fraction)
        self.talys_runner = talys.Runner(self.element.symbol, self.mass_number)

    def material_term(self):
        return (N_A * self.fraction) / self.mass_number

    def differential_n_spec(
        self, alpha_energy, run_talys=False, force_recalculation=False
    ):
        rounded_alpha_energy = int(100 * alpha_energy) / 100.0

        if force_recalculation:
            self.talys_runner.run(rounded_alpha_energy)

        spectra_file_path = self.talys_runner.spectra_file(rounded_alpha_energy)
        if not os.path.exists(spectra_file_path):
            if run_talys:
                attempts = 0
                while attempts < 3 and not os.path.exists(spectra_file_path):
                    self.talys_runner.run(rounded_alpha_energy)
                    attempts += 1

                # If all three attempts to run TALYS failed, exit early
                if attempts == 3:
                    return {}
            else:
                return {}

        # This should be impossible to reach because the TALYS runner creates
        # all of these directories on instantiation. TODO: verify then remove
        if not os.path.exists(self.talys_runner.output_dir):
            return {}

        spectra_file = open(spectra_file_path)
        spectra = {}

        for spec in [line.split() for line in spectra_file.readlines()]:
            if spec == [] or spec[0] == "EMPTY":
                break
            elif spec[0][0] == "#":
                continue

            energy = int(float(spec[0]) * MeV_to_keV)
            sigma = float(spec[1]) * mb_to_cm2 / MeV_to_keV

            spectra[energy] = sigma

        return spectra

    def cross_section(self, alpha_energy):
        rounded_alpha_energy = int(100 * alpha_energy) / 100.0

        output_file_path = self.talys_runner.output_file(rounded_alpha_energy)

        if not os.path.exists(output_file_path):
            return 0

        with open(output_file_path, "r") as output_file:
            file_text = output_file.read()

        if cross_section_match := re.search(NEUTRON_CROSS_SECTION_PATTERN, file_text):
            cross_section = float(cross_section_match.group("cross_section"))

            return cross_section * mb_to_cm2
        else:
            return 0


class StoppingPowerList:
    def __init__(self, element_symbol):
        self.element_symbol = element_symbol
        self.stopping_powers = {}

    def load_file(self):
        file_path = f"./Data/StoppingPowers/{self.element_symbol.lower()}.dat"
        file = open(file_path)

        for data in [
            line.split() for line in file.readlines() if not line.startswith("#")
        ]:
            energy = float(data[0])
            units = str(data[1])
            stopping_power = float(data[2]) + float(data[3])

            if units == "keV":
                energy /= 1000

            self.stopping_powers[energy] = stopping_power

    # Use binary search to find energy in log(N) time
    def for_alpha(self, alpha_energy):
        energy_intervals = list(self.stopping_powers.keys())
        min_energy = energy_intervals[0]
        max_energy = energy_intervals[-1]

        if alpha_energy < min_energy:
            return self.stopping_powers[min_energy]
        elif alpha_energy > max_energy:
            return self.stopping_powers[max_energy]

        range_end = bisect(energy_intervals, alpha_energy)
        range_start = range_end - 1

        energy_start = energy_intervals[range_start]
        energy_end = energy_intervals[range_end]
        energy_diff = (alpha_energy - energy_start) / (energy_end - energy_start)

        stop_power_start = self.stopping_powers[energy_start]
        stop_power_end = self.stopping_powers[energy_end]

        return (stop_power_end - stop_power_start) * energy_diff + stop_power_start


class Composition:
    @classmethod
    def from_file(cls, file_path):
        file = open(file_path)

        composition = cls()

        for material in [
            line.split() for line in file.readlines() if not line.startswith("#")
        ]:
            if len(material) < 3:
                continue

            element = elements.Element(material[0])
            mass_number = int(material[1])
            fraction = float(material[2])

            # If a single mass number isn't specified, use all isotopes
            # along with their natural abundances
            if mass_number == 0:
                for isotope in element.isotopes():
                    composition.add(
                        Isotope(
                            element,
                            isotope,
                            fraction * element.abundance(isotope) / 100.0,
                        )
                    )

            # Otherwise, if a single mass number is provided,
            # use the fraction provided
            else:
                composition.add(
                    Isotope(
                        element,
                        mass_number,
                        fraction / 100.0,
                    )
                )

        composition.normalize()
        composition.populate_stopping_powers()

        return composition

    def __init__(self):
        self.materials = []
        self.fractions = {}
        self.stopping_powers = {}

    def normalize(self):
        norm = 0

        for material in self.materials:
            norm += material.fraction

        for material in self.materials:
            material.fraction /= norm

            # Computes the fraction of this element in the overall material,
            # grouping isotopes with the same Z
            symbol = material.element.symbol
            self.fractions[symbol] = self.fractions.get(symbol, 0) + material.fraction

    def populate_stopping_powers(self):
        # Populates stopping powers from ./Data/StoppingPowers once so that
        # they don't need to be populated for every energy step
        for element in self.fractions:
            stop_power_list = StoppingPowerList(element)
            stop_power_list.load_file()

            self.stopping_powers[element] = stop_power_list

    def empty(self):
        return len(self.materials) == 0

    def add(self, material):
        self.materials.append(material)

    # Expects an alpha energy in units of MeV
    def stopping_power(self, e_alpha):
        total_stopping_power = 0

        for element, fraction in self.fractions.items():
            element_stop_power = self.stopping_powers[element].for_alpha(e_alpha)

            total_stopping_power += element_stop_power * fraction

        return total_stopping_power
