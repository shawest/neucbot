import glob
import os
import re
import subprocess

from string import Template

from neucbot import utils
from neucbot.data.data_source import NeucbotDataSource

command_template = Template(
    """
projectile a
ejectiles p n g
element $element
mass $mass_number
energy $alpha_energy
preequilibrium y
giantresonance y
multipreeq y
outspectra y
outlevels y
outgamdis y
filespectrum n
elwidth 0.2
"""
)

mb_to_cm2 = 1.0e-27
MeV_to_keV = 1.0e3
ISOTOPES_DIR = "./Data/Isotopes"

NEUTRON_CROSS_SECTION_PATTERN = re.compile(
    r"2. Binary non-elastic cross sections .non-exclusive.\n\n\s+gamma.*\n\s+neutron = (?P<cross_section>\d\.\d{5}E[\+\-]\d{2})"
)


class RawTalysDataSource(NeucbotDataSource):
    def __init__(self, element, mass_number):
        # Sets properties required of all NeucbotDataSource implementations
        super().__init__(element, mass_number)

        # Properties specific to the RawTalysDataSource
        self.iso = self.element + str(self.mass_number)
        self.base_dir = os.path.join(ISOTOPES_DIR, self.element, self.iso)
        self.input_dir = os.path.join(self.base_dir, "TalysInputs")
        self.output_dir = os.path.join(self.base_dir, "TalysOut")
        self.spectra_dir = os.path.join(self.base_dir, "NSpectra")

        self.ensure_dirs_exist()

    # Methods defined by abstract class:
    # - cross_section
    # - nspectra
    # - download_data
    # - allows_talys_calculation
    def cross_section(self, rounded_alpha_energy):
        output_file_path = self.output_file(rounded_alpha_energy)

        if not os.path.exists(output_file_path):
            return 0

        with open(output_file_path, "r") as output_file:
            file_text = output_file.read()

        if cross_section_match := re.search(NEUTRON_CROSS_SECTION_PATTERN, file_text):
            cross_section = float(cross_section_match.group("cross_section"))

            return cross_section * mb_to_cm2
        else:
            return 0

    def nspectra(self, rounded_alpha_energy):
        spectra_file_path = self.spectra_file(rounded_alpha_energy)

        if not os.path.exists(spectra_file_path):
            return utils.Histogram()

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

        return utils.Histogram(spectra)

    def download_data(self, version="v2"):
        if not (os.listdir(self.output_dir) and os.listdir(self.spectra_dir)):
            print(f"Downloading (dataset {version}) full TALYS data for {self.element}")
            subprocess.call(
                f"./Scripts/download_element_{version}.sh {self.element}", shell=True
            )

    def allows_talys_calculation(self):
        return True

    # Helper methods specific to this data source
    def ensure_dirs_exist(self):
        for directory in [self.input_dir, self.output_dir, self.spectra_dir]:
            os.makedirs(directory, exist_ok=True)

    def input_file(self, alpha_energy):
        return os.path.join(self.input_dir, f"inputE{alpha_energy}")

    def output_file(self, alpha_energy):
        return os.path.join(self.output_dir, f"outputE{alpha_energy}")

    def spectra_file(self, alpha_energy):
        return os.path.join(
            self.spectra_dir, "nspec{0:0>7.3f}.tot".format(alpha_energy)
        )

    def run_talys(self, alpha_energy):
        input_file_path = self.input_file(alpha_energy)
        output_file_path = self.output_file(alpha_energy)

        # Write talys input file
        input_file = open(input_file_path, "w")
        input_file.write(
            command_template.substitute(
                element=self.element,
                mass_number=self.mass_number,
                alpha_energy=alpha_energy,
            )
        )
        input_file.close()

        talys_command = f"talys < {input_file_path} > {output_file_path}"

        # Run talys command to generate files
        result = subprocess.call(talys_command, shell=True)

        # Check result for successful exit
        if result == 0:
            print(f"Successfully ran command: {talys_command}")
        else:
            raise RuntimeError(f"Failed TALYS command: {talys_command}")

        # Move TALYS files to expected output
        generated_nspec_files = glob.glob(".*nspec.*")
        nspec_file_path = self.spectra_file(alpha_energy)

        if generated_nspec_files and len(generated_nspec_files) == 1:
            os.replace(generated_nspec_files[0], nspec_file_path)
        else:
            nspec_file = open(nspec_file_path, "w")
            nspec_file.write("EMPTY")
            nspec_file.close()

    def run_talys_with_retries(self, alpha_energy, retry_count=3):
        spectra_file = self.spectra_file(alpha_energy)
        while retry_count > 0 and not os.path.exists(spectra_file):
            self.run_talys(alpha_energy)
            retry_count -= 1
