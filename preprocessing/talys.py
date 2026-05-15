import os
import re
import json
import subprocess
import shutil

from neucbot.data.raw_talys import (
    ISOTOPES_DIR,
    NEUTRON_CROSS_SECTION_PATTERN,
    mb_to_cm2,
    MeV_to_keV,
)

TALYS_OUT_JSON_PATH = "./Data/TalysSlim/TalysOut/"
TALYS_NSPEC_JSON_PATH = "./Data/TalysSlim/NSpec/"


class TalysPreprocessor:
    def __init__(self, element):
        self.element = element

        # Input Directories
        self.base_dir = os.path.join(ISOTOPES_DIR, element)

        # Preprocessing Output Directories
        self.preproc_talys_out_dir = os.path.join(TALYS_OUT_JSON_PATH, self.element)
        self.preproc_talys_nspec_dir = os.path.join(TALYS_NSPEC_JSON_PATH, self.element)
        os.makedirs(self.preproc_talys_out_dir, exist_ok=True)
        os.makedirs(self.preproc_talys_nspec_dir, exist_ok=True)

    # Preprocessing File Output paths
    def preproc_talys_out_filepath(self, mass_number):
        return os.path.join(TALYS_OUT_JSON_PATH, self.element, f"{mass_number}.json")

    def preproc_talys_nspec_filepath(self, mass_number):
        return os.path.join(TALYS_NSPEC_JSON_PATH, self.element, f"{mass_number}.json")

    # TALYS complete data methods
    def download_v2_if_not_present(self):
        if not os.path.exists(f"./Data/Isotopes/{self.element}"):
            print("Downloading TALYS outputs for:", self.element)
            subprocess.call(
                f"./Scripts/download_element_v2.sh {self.element}", shell=True
            )
        else:
            print(f"Data already exists for {self.element}")

    def download_v1_if_not_present(self):
        if not os.path.exists(f"./Data/Isotopes/{self.element}"):
            print("Downloading TALYS outputs for:", self.element)
            subprocess.call(
                f"./Scripts/download_element_v1.sh {self.element}", shell=True
            )
        else:
            print(f"Data already exists for {self.element}")

    def talys_full_data_exists(self, mass_number):
        talys_full_out_exists = os.path.exists(self.talys_output_dir(mass_number))
        talys_full_nspec_exists = os.path.exists(self.talys_nspec_dir(mass_number))

        return talys_full_out_exists and talys_full_nspec_exists

    def clean_isotope_data(self):
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)

    def processed_files_exist(self):
        talys_out_exists = os.path.exists(self.preproc_talys_out_dir) and os.listdir(
            self.preproc_talys_out_dir
        )
        talys_nspec_exists = os.path.exists(
            self.preproc_talys_nspec_dir
        ) and os.listdir(self.preproc_talys_nspec_dir)

        return talys_out_exists and talys_nspec_exists

    def talys_output_dir(self, mass_number):
        return os.path.join(self.base_dir, f"{self.element}{mass_number}", "TalysOut")

    def talys_nspec_dir(self, mass_number):
        return os.path.join(self.base_dir, f"{self.element}{mass_number}", "NSpectra")

    # Preprocessing methods
    def process_talys_nspec(self, mass_number):
        spectra = {}

        talys_nspec_dir = self.talys_nspec_dir(mass_number)
        print(talys_nspec_dir)

        if not os.path.exists(talys_nspec_dir):
            UNPROCESSED_NSPEC_ELEMENTS.append(self.element + str(mass_number))
            return

        with os.scandir(talys_nspec_dir) as files:
            for file in files:
                if file.is_file() and file.name.startswith("nspec"):
                    rounded_energy = float(
                        file.name.removeprefix("nspec").removesuffix(".tot")
                    )

                    energy_spec = {}

                    file_path = os.path.join(talys_nspec_dir, file.name)

                    with open(file_path, "r") as output_file:
                        for spec in [line.split() for line in output_file.readlines()]:
                            if spec == [] or spec[0] == "EMPTY":
                                break
                            elif spec[0][0] == "#":
                                continue

                            energy = int(float(spec[0]) * MeV_to_keV)
                            sigma = float(spec[1]) * mb_to_cm2 / MeV_to_keV

                            energy_spec[energy] = sigma

                    spectra[rounded_energy] = energy_spec

        with open(self.preproc_talys_nspec_filepath(mass_number), "w") as out_file:
            json.dump(spectra, out_file, sort_keys=True, indent=2)

    def process_talys_out(self, mass_number):
        cross_sections = {}

        talys_output_dir = self.talys_output_dir(mass_number)

        if not os.path.exists(talys_output_dir):
            UNPROCESSED_NSPEC_ELEMENTS.append(self.element + str(mass_number))
            return

        with os.scandir(talys_output_dir) as files:
            for file in files:
                if file.is_file() and file.name.startswith("outputE"):
                    rounded_energy = file.name.removeprefix("outputE")

                    file_path = os.path.join(talys_output_dir, file.name)

                    with open(file_path, "r") as output_file:
                        file_text = output_file.read()

                    if cross_section_match := re.search(
                        NEUTRON_CROSS_SECTION_PATTERN, file_text
                    ):
                        cross_section = float(
                            cross_section_match.group("cross_section")
                        )

                        cross_sections[rounded_energy] = cross_section * mb_to_cm2
                    else:
                        cross_sections[rounded_energy] = 0

        with open(self.preproc_talys_out_filepath(mass_number), "w") as out_file:
            json.dump(cross_sections, out_file, sort_keys=True, indent=2)
