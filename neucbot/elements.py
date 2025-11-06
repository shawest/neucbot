import json

from neucbot import chemistry

"""
Reads in the map from elements.json, which is structured in the following format:

{
  "H": {
    "1": {
      "z": 1,
      "abundance": 99.985
    },
    "2": {
      "z": 1,
      "abundance": 0.015
    }
  },
  "He": {
    "3": {
      "z": 2,
      "abundance": 0.000137
    },
    ...
  },
  ...
}
"""

with open("./neucbot/elements.json", "r") as file:
    isotopesMap = json.load(file)

class Element:
    def __init__(self, element):
        self.symbol = element.capitalize()
        self.isos = isotopesMap.get(self.symbol)

    def isotopes(self):
        return [iso for iso in self.isos.keys()]

    def abundance(self, isotope):
        return float(self.isos.get(isotope).get("abundance"))
