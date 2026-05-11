import json

from neucbot import alpha

if __name__ == "__main__":
    with open("./neucbot/elements.json", "r") as file:
        isotopesMap = json.load(file)

        for element, isoMap in isotopesMap.items():
            for mass_number in isoMap:
                try:
                    print("Downloading AlphaList file for:", element, mass_number)
                    alpha.AlphaList(element, mass_number).write()
                except RuntimeError:
                    print("No AlphaList file for:", element, mass_number)
