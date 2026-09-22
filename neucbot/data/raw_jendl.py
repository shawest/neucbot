import glob
import os
import re
import subprocess

from bisect import bisect

from neucbot import utils
from neucbot.data.data_source import NeucbotDataSource

mb_to_cm2 = 1.0e-27
MeV_to_keV = 1.0e3
ISOTOPES_DIR = "./Data/Isotopes"
JENDL_OUT_DIR = "JendlOut"
JENDL_OUT_SUBDIR = "MT4"


class RawJendlDataSource(NeucbotDataSource):
    def __init__(self, element, mass_number):
        # Sets properties required of all NeucbotDataSource implementations
        super().__init__(element, mass_number)

        self.iso = self.element + str(self.mass_number)
        self.base_dir = os.path.join(ISOTOPES_DIR, self.element)
        self.output_dir = os.path.join(
            self.base_dir, self.iso, JENDL_OUT_DIR, JENDL_OUT_SUBDIR
        )

        self.ensure_dirs_exist()

    def cross_section(self, rounded_alpha_energy):
        if not hasattr(self, "cross_sections"):
            return 0

        # This if statement would be captured by the else block, but can improve
        # performance slightly by skipping the binary search
        if exact_match := self.cross_sections.get(rounded_alpha_energy):
            return exact_match

        # If alpha energy is not an exact match, find the greatest energy in the
        # JENDL file that is less than the input alpha_energy and use that
        else:
            energies = list(self.cross_sections.keys())
            energy_index = bisect(energies, rounded_alpha_energy) - 1
            energy = energies[energy_index]

            return self.cross_sections.get(energy)

    def nspectra(self, rounded_alpha_energy):
        output_file_path = self.output_file(rounded_alpha_energy)

        if not os.path.exists(output_file_path):
            return utils.Histogram()

        output_file = open(output_file_path)
        spectra = {}

        for spec in [line.split() for line in output_file.readlines()]:
            if spec == [] or spec[0] == "EMPTY":
                break
            elif spec[0][0] == "#":
                continue

            energy = int(float(spec[0]) * MeV_to_keV)
            sigma = float(spec[1]) * mb_to_cm2 / MeV_to_keV

            spectra[energy] = sigma

        return utils.Histogram(spectra)

    def download_data(self, version):  # Version not needed, fix this
        jendl_data_pattern = os.path.join(
            self.base_dir, "*", JENDL_OUT_DIR, JENDL_OUT_SUBDIR, "outputE*"
        )
        jendl_data = glob.glob(jendl_data_pattern)

        if len(jendl_data) == 0:
            print(f"Downloading full JENDL data for {self.element}")
            subprocess.call(
                f"./Scripts/download_jendl_data.sh {self.element}", shell=True
            )

        self.set_cross_sections()

    def allows_talys_calculation(self):
        return False

    # Helper methods specific to this data source
    def ensure_dirs_exist(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def output_file(self, alpha_energy):
        return os.path.join(self.output_dir, f"outputE{alpha_energy:.4f}")

    def cross_section_file(self):
        return os.path.join(self.output_dir, "cross-section")

    def set_cross_sections(self):
        if not os.path.exists(self.cross_section_file()):
            print(f"No JENDL cross section file found for {self.iso}")
            return

        cross_file = open(self.cross_section_file())
        cross_sections = {}

        for cross_section in [line.split() for line in cross_file.readlines()]:
            if cross_section[0][0] == "#":
                continue

            energy = float(cross_section[0])
            sigma = float(cross_section[1]) * mb_to_cm2

            cross_sections[energy] = sigma

        cross_file.close()

        self.cross_sections = cross_sections
