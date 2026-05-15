import json
import os
import requests
import shutil
import tarfile

from functools import cached_property

from neucbot import utils

from neucbot.data.data_source import NeucbotDataSource

TALYS_SLIM_VERSION = "0.0.1"
TALYS_SLIM_URL = f"https://github.com/mpiercy827/talys_slim/archive/refs/tags/v{TALYS_SLIM_VERSION}.tar.gz"
TALYS_SLIM_TAR_PATH = "talys_slim.tar.gz"
TALYS_SLIM_DESTINATION = "./Data"


class TalysSlimDataSource(NeucbotDataSource):
    def __init__(self, element, mass_number):
        # Required properties
        self.element = element
        self.mass_number = mass_number

        # Properties specific to this data source
        self.base_dir = os.path.join("Data", "TalysSlim")

    def cross_section(self, rounded_alpha_energy):
        return self.talys_outputs.get(rounded_alpha_energy, 0)

    def nspectra(self, rounded_alpha_energy):
        spectra = self.talys_nspec.get(rounded_alpha_energy, {})
        return utils.Histogram(spectra)

    def download_data(self, version=None):
        if os.path.exists(self.base_dir) and os.listdir(self.base_dir):
            return

        print(f"Downloading talys_slim v{TALYS_SLIM_VERSION}")
        response = requests.get(TALYS_SLIM_URL)
        with open(TALYS_SLIM_TAR_PATH, "wb") as tar_file:
            tar_file.write(response.content)

        with tarfile.open(TALYS_SLIM_TAR_PATH) as tar:
            print("Extracting talys_slim tarfile")
            tar.extractall()
            shutil.move(f"talys_slim-{TALYS_SLIM_VERSION}/TalysSlim/", "./Data")

        # cleanup files
        print("Cleaning TalysSlim files...")
        os.remove(TALYS_SLIM_TAR_PATH)
        shutil.rmtree(f"talys_slim-{TALYS_SLIM_VERSION}")

    def allows_talys_calculation(self):
        return False

    # Helper methods for this datasource
    @cached_property
    def talys_outputs(self):
        output_file_path = os.path.join(
            self.base_dir, "TalysOut", self.element, f"{self.mass_number}.json"
        )
        with open(output_file_path) as output_file:
            return json.load(output_file, object_hook=self.transform_keys)

    @cached_property
    def talys_nspec(self):
        spectra_file_path = os.path.join(
            self.base_dir, "NSpec", self.element, f"{self.mass_number}.json"
        )
        with open(spectra_file_path) as spectra_file:
            return json.load(spectra_file, object_hook=self.transform_keys)

    # Helper function for parsing keys as floats, not strings
    def transform_keys(self, data):
        return {float(key): value for key, value in data.items()}
