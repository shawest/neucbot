"""
Functionality related to the National Nuclear Data Center's (NNDC) Evaluated
Nuclear Structure Data Files (ENSDF). More information about record structure
can be found at:

https://www.nndc.bnl.gov/ensdf/ensdf-manual.pdf
"""
import os
import re
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

from neucbot import elements

"""
www.nndc.bnl.gov will reject requests with a 429 response when the 'User-Agent'
header is set to the default python value, so this is sent to work around that.
"""
REQUEST_HEADERS = {"User-Agent": "neucbot"}
URL_BASE = "https://www.nndc.bnl.gov/nudat3/"
DECAY_SEARCH_URL = "decaysearchdirect.jsp"
ALPHA_DECAY_HREF_PATTERN = re.compile("getdecaydataset.jsp" + ".*a\\sdecay")

DECAY_DATA_DIR = "./Data/Decays/ensdf"
ALPHA_LIST_DIR = "./AlphaLists"

class Client:
    def __init__(self, element, isotope):
        self.element = elements.Element(element)
        self.isotope = str(isotope)
        self.nndc_url = URL_BASE + DECAY_SEARCH_URL + "?unc=NDS&nuc=" + self.isotope + element.upper()
        self.http = self.setup_http()

    def write_alpha_files(self):
        alpha_list_file = self.alpha_list_file_path()

        if os.path.exists(alpha_list_file):
            print(f"Alpha list file already exists at {self.alpha_list_file_path()}")
        else:
            decay_file_text = self.read_or_fetch_decay_file()
            energyMaps = Parser.parse(decay_file_text)
            file = open(alpha_list_file, "w")

            for energy, probability in energyMaps["alphas"].items():
                file.write(f"{str(energy/1000)}\t{probability}\n")

            file.close()

        return True

    def read_or_fetch_decay_file(self):
        if os.path.exists(self.decay_file_path()):
            file = open(self.decay_file_path(), "r")
            decay_file_text = file.read()
            file.close()

            return decay_file_text
        else:
            return self.fetch_and_write_decay_file()

    def fetch_and_write_decay_file(self):
        search_results = self.http.get(self.nndc_url, headers=REQUEST_HEADERS).content
        links = BeautifulSoup(search_results, "html.parser").find_all(href=ALPHA_DECAY_HREF_PATTERN)

        if len(links) == 0:
            raise RuntimeError(f"No Alpha Decay links found on {self.nndc_url}")
        else:
            for link in links:
                path = link.attrs.get("href")
                decay_page = self.http.get(URL_BASE + path, headers=REQUEST_HEADERS).text
                decay_file = BeautifulSoup(decay_page, "html.parser").find("pre")

                if decay_file and len(decay_file.contents) > 0:
                    decay_file = decay_file.contents[0].strip()
                else:
                    raise RuntimeError(f"No page content found on {self.nndc_url}{path}")

                if not Parser.is_alpha_decay(decay_file):
                    print(f"No alpha decay found at {self.nndc_url}/{path}")
                elif not Parser.is_ground_state_decay(decay_file):
                    print(f"No ground state decay found at {self.nndc_url}/{path}")
                else:
                    return self.write_decay_file(decay_file)

        raise RuntimeError(f"No valid ground state alpha decays found at {self.nndc_url}")

    def write_decay_file(self, decay_file_text):
        file = open(self.decay_file_path(), "w")
        file.write(str(decay_file_text))
        file.close()

        return decay_file_text

    def decay_file_path(self):
        return f"{DECAY_DATA_DIR}/{self.element.symbol}{self.isotope}.dat"

    def alpha_list_file_path(self):
        return f"{ALPHA_LIST_DIR}/{self.element.symbol}{self.isotope}Alphas.dat"

    def setup_http(self):
        session = Session()
        session.mount("https://", HTTPAdapter(max_retries=Retry(total=3)))

        return session


"""
The Parser class parses records from the NNDC ENSDF Database
"""
class Parser:

    # Pattern of Parent Record for Ground State Decay is:
    # "(5-character nuclear ID)  P (0.0 + whitespace)"
    # ENSDF Manual, page 17
    GROUND_STATE_DECAY_RECORD = re.compile(r"^[A-Z0-9]{5}\s{2}P\s([0\.\s]){10}")

    # Pattern of Intensity is:
    # "(5-character nuclear ID)  N (Intensity [up to 10 digits])"
    # ENSDF Manual, page 18-19
    INTENSITY_RECORD = re.compile(r"^[A-Z0-9]{5}\s{2}N\s(?P<intensity>[0-9\.\s]{10})")

    # Pattern of Alpha energies is:
    # "(5-character nuclear ID)  A (Energy [up to 10 digits]) (Uncertainty Energy) (Intensity) (Uncertainty intensity)"
    # ENSDF Manual, page 25
    ALPHA_RECORD = re.compile(r"^[A-Z0-9]{5}\s{2}A\s(?P<energy>[0-9\s\.]{10})[0-9\.\s]{2}(?P<intensity>[0-9\.\-E\s]{8})")

    # Pattern of Gamma energies is:
    # "(5-character nuclear ID)  G (Energy [up to 10 digits]) (Uncertainty Energy) (Intensity) (Uncertainty intensity)"
    # ENSDF Manual, page 28
    GAMMA_RECORD = re.compile(r"^[A-Z0-9]{5}\s{2}G\s(?P<energy>[0-9\s\.]{10})[0-9\.\s]{2}(?P<intensity>[0-9\.\-E\s]{8})")

    @classmethod
    def parse(cls, file_text):
        contents = { "alphas": {}, "gammas": {}, "intensity": 0 }
        for line in file_text.splitlines():
            if cls.questionable_record(line):
                continue

            if intensity_match := cls.INTENSITY_RECORD.match(line):
                intensity = intensity_match.group("intensity").strip()

                if intensity == "":
                    intensity = 1.0

                contents["intensity"] = float(intensity)

            elif alpha_match := cls.ALPHA_RECORD.match(line):
                energy = float(alpha_match.group("energy"))
                intensity = float(alpha_match.group("intensity"))

                contents["alphas"][energy] = intensity

            elif gamma_match := cls.GAMMA_RECORD.match(line):
                energy = float(gamma_match.group("energy"))
                intensity = gamma_match.group("intensity").strip()

                if intensity == "":
                    continue

                contents["gammas"][energy] = float(intensity) * contents["intensity"]

        return contents

    @classmethod
    def questionable_record(cls, record):
        return len(record) > 77 and record[-1] == "?"

    @classmethod
    def is_alpha_decay(cls, page_text):
        return page_text.splitlines()[0].find(" A DECAY") != -1

    @classmethod
    def is_ground_state_decay(cls, page_text):
        return any(cls.GROUND_STATE_DECAY_RECORD.match(line) for line in page_text.splitlines())

