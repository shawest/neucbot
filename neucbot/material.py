import os
import re
import subprocess

from bisect import bisect

from neucbot import elements
from neucbot import utils

N_A = 6.0221409e23


class Isotope:
    # self.fraction should be a number between 0 and 1
    def __init__(self, element, mass_number, fraction, data_source_class):
        self.element = element
        self.mass_number = int(mass_number)
        self.fraction = float(fraction)
        self.data_source = data_source_class(element.symbol, mass_number)

    def material_term(self):
        return (N_A * self.fraction) / self.mass_number

    def name(self):
        return f"{self.element.symbol}{self.mass_number}"

    def differential_n_spec(
        self, alpha_energy, run_talys=False, force_recalculation=False
    ):
        rounded_alpha_energy = int(100 * alpha_energy) / 100.0

        if self.data_source.allows_talys_calculation():
            if force_recalculation:
                self.data_source.run_talys(rounded_alpha_energy)
            elif run_talys:
                self.data_source.run_talys_with_retries(rounded_alpha_energy)

        return self.data_source.nspectra(rounded_alpha_energy)

    def cross_section(self, alpha_energy):
        rounded_alpha_energy = int(100 * alpha_energy) / 100.0
        return self.data_source.cross_section(rounded_alpha_energy)

    def download_data(self, version=None):
        self.data_source.download_data(version)


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
    def from_file(cls, file_path, data_source_class):
        file = open(file_path)

        composition = cls(data_source_class)

        for material in [
            line.split() for line in file.readlines() if not line.startswith("#")
        ]:
            if len(material) < 3:
                continue

            composition.add(
                {
                    "element": material[0],
                    "mass_number": material[1],
                    "fraction": material[2],
                }
            )

        composition.normalize()
        composition.populate_stopping_powers()

        return composition

    @classmethod
    def from_json(cls, request_json, data_source_class):
        composition = cls(data_source_class)

        for material_element in request_json["elements"]:
            composition.add(material_element)

        composition.normalize()
        composition.populate_stopping_powers()

        return composition

    def __init__(self, data_source_class):
        self.data_source_class = data_source_class
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

    def add(self, material_element):
        element = elements.Element(material_element["element"])
        mass_number = int(material_element["mass_number"])
        fraction = float(material_element["fraction"])

        # If a single mass number isn't specified, use all isotopes
        # along with their natural abundances
        if mass_number == 0:
            for isotope in element.isotopes():
                self.materials.append(
                    Isotope(
                        element,
                        isotope,
                        fraction * element.abundance(isotope) / 100.0,
                        self.data_source_class,
                    )
                )

        # Otherwise, if a single mass number is provided,
        # use the fraction provided
        else:
            self.materials.append(
                Isotope(element, mass_number, fraction / 100.0, self.data_source_class)
            )

    # Expects an alpha energy in units of MeV
    def stopping_power(self, e_alpha):
        total_stopping_power = 0

        for element, fraction in self.fractions.items():
            element_stop_power = self.stopping_powers[element].for_alpha(e_alpha)

            total_stopping_power += element_stop_power * fraction

        return total_stopping_power

    def download_data(self, version=None):
        for material in self.materials:
            material.download_data(version)
