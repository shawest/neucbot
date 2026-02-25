import glob
import os
import subprocess

from string import Template

ISOTOPES_DIR = "./Data/Isotopes"

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


class Runner:
    def __init__(self, element, mass_number):
        iso = element + str(mass_number)
        base_path = os.path.join(ISOTOPES_DIR, element, iso)

        self.element = element
        self.mass_number = mass_number
        self.input_dir = os.path.join(base_path, "TalysInputs")
        self.output_dir = os.path.join(base_path, "TalysOut")
        self.spectra_dir = os.path.join(base_path, "NSpectra")

        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.spectra_dir, exist_ok=True)

    def run(self, alpha_energy):
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

    def input_file(self, alpha_energy):
        return os.path.join(self.input_dir, f"inputE{alpha_energy}")

    def output_file(self, alpha_energy):
        return os.path.join(self.output_dir, f"outputE{alpha_energy}")

    def spectra_file(self, alpha_energy):
        return os.path.join(
            self.spectra_dir, "nspec{0:0>7.3f}.tot".format(alpha_energy)
        )
