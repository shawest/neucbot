import json

from preprocessing import talys

with open("./neucbot/elements.json", "r") as file:
    isotopesMap = json.load(file)


if __name__ == "__main__":
    for element, isoMap in isotopesMap.items():
        preproc = talys.TalysPreprocessor(element)

        # Skip if already preprocessed
        if preproc.processed_files_exist():
            print("Already computed for ", element)
            continue

        # Download complete TALYS data if not present
        preproc.download_v2_if_not_present()
        preproc.download_v1_if_not_present()

        # Perform preprocessing
        for mass_number in isoMap:

            # Skip this element/mass_number if TALYS data is not available for it
            if not preproc.talys_full_data_exists(mass_number):
                print("Unable to preprocess TALYS data for:", element, mass_number)
                continue

            print("Processing TALYS outputs for:", element, mass_number)
            preproc.process_talys_out(mass_number)
            preproc.process_talys_nspec(mass_number)

        # Clean up complete TALYS data to free up disk space
        preproc.clean_isotope_data()
