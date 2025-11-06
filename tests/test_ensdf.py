import pytest
import re

from unittest import TestCase
from unittest.mock import call, Mock, patch
from requests import Session
from requests.exceptions import HTTPError
from neucbot.ensdf import Client, Parser, REQUEST_HEADERS, URL_BASE

class MockResponse:
    def __init__(self, content):
        self.content = content
        self.text = content

class MockSearchResponse():
    def __init__(self):
        with open("./tests/test_ensdf/bi212_search_results.html", "r") as file:
            self.content = file.read()

class MockDecayResponse():
    def __init__(self):
        with open("./tests/test_ensdf/bi212.html", "r") as file:
            self.text = file.read()

def ensdf_fetch_success(url, headers):
    if re.search(r"decaysearchdirect", url):
        return MockSearchResponse()
    elif re.search(r"getdecaydataset", url):
        return MockDecayResponse()

def ensdf_fetch_empty_decay(url, headers):
    if re.search(r"decaysearchdirect", url):
        return MockSearchResponse()
    elif re.search(r"getdecaydataset", url):
        return MockResponse("<html><body><pre></pre></body></html>")

@patch("os.path.exists")
class TestClient(TestCase):

    @patch.object(Session, "get")
    def test_write_alpha_files_success(self, mocked_get, mocked_os_path_exists):
        # Assume no decay or alpha files exist
        mocked_os_path_exists.return_value = False

        # First return search HTML, then decay HTML
        mocked_get.side_effect = ensdf_fetch_success

        client = Client("Bi", 212)
        client.write_alpha_files()

        mocked_get.assert_has_calls([
            call(client.nndc_url, headers=REQUEST_HEADERS),
            call(URL_BASE + "getdecaydataset.jsp?nucleus=208TL&dsid=212bi a decay (25.0 m)", headers=REQUEST_HEADERS),
        ])


    @patch.object(Client, "fetch_and_write_decay_file")
    def test_reads_existing_decay_file(self, mocked_client_fetch, mocked_os_path_exists):
        def decay_file_exists(path):
            return re.search(r"Data\/Decays", path)

        mocked_os_path_exists.side_effect = decay_file_exists

        client = Client("Bi", 212)
        client.write_alpha_files()

        mocked_client_fetch.assert_not_called()
        mocked_os_path_exists.assert_has_calls([
            call("./AlphaLists/Bi212Alphas.dat"),
            call("./Data/Decays/ensdf/Bi212.dat"),
        ])


    @patch.object(Session, "get")
    def test_raises_runtime_error_for_no_alpha_decay_links(self, mocked_get, mocked_os_path_exists):
        # Assume no decay or alpha files exist
        mocked_os_path_exists.return_value = False

        # Mimic search for invalid element
        mocked_get.return_value = MockResponse("<html><body>No datasets were found within the specified search parameters</body></html>")

        client = Client("Bi", 212)

        with self.assertRaisesRegex(RuntimeError, r"No Alpha Decay links found"):
            client.write_alpha_files()


    @patch.object(Session, "get")
    def test_empty_decay_page_content(self, mocked_get, mocked_os_path_exists):
        # Assume no decay or alpha files exist
        mocked_os_path_exists.return_value = False

        # First return search HTML, then empty decay HTML
        mocked_get.side_effect = ensdf_fetch_empty_decay

        client = Client("Bi", 212)

        with self.assertRaisesRegex(RuntimeError, r"No page content found"):
            client.write_alpha_files()


    @patch.object(Parser, "is_alpha_decay")
    @patch.object(Session, "get")
    def test_not_alpha_decay_file(self, mocked_get, mocked_alpha_decay, mocked_os_path_exists):
        mocked_os_path_exists.return_value = False
        mocked_get.side_effect = ensdf_fetch_success
        mocked_alpha_decay.return_value = False

        client = Client("Bi", 212)

        with self.assertRaisesRegex(RuntimeError, r"No valid ground state alpha decays"):
            client.write_alpha_files()


    @patch.object(Parser, "is_ground_state_decay")
    @patch.object(Parser, "is_alpha_decay")
    @patch.object(Session, "get")
    def test_not_ground_state_decay_file(self, mocked_get, mocked_alpha_decay, mocked_ground_state, mocked_os_path_exists):
        mocked_os_path_exists.return_value = False
        mocked_get.side_effect = ensdf_fetch_success
        mocked_alpha_decay.return_value = True
        mocked_ground_state.return_value = False

        client = Client("Bi", 212)

        with self.assertRaisesRegex(RuntimeError, r"No valid ground state alpha decays"):
            client.write_alpha_files()


    @patch.object(Session, "get")
    def test_retry_on_http_errors(self, mocked_get, mocked_os_path_exists):
        mocked_os_path_exists.return_value = False
        mocked_get.side_effect = [
            HTTPError("500 Internal Server Error"),
            MockSearchResponse(),
            MockDecayResponse(),
        ]

        client = Client("Bi", 212)

        try:
            client.write_alpha_files()
        except HTTPError:
            pass

        client.write_alpha_files()

        self.assertEqual(mocked_get.call_count, 3)


class TestParser(TestCase):
    def test_parse(self):
        with open("./tests/test_ensdf/bi212.txt", "r") as file:
            text = file.read()

        expected_alphas = {
                6089.88: 27.12,
                6050.78: 69.91,
                5768: 1.70,
                5626: 0.157,
                5607: 1.13,
                5481: 0.013,
                5345: 0.0010,
                5302: 0.00011,
                }
        expected_gammas = {
  	            39.857: 2.96,
  	            288.2: 0.938,
  	            328.03: 0.349,
  	            433.7: 0.047,
  	            452.98: 1.01,
  	            473.0: 0.14,
                }

        expected = { "alphas": expected_alphas, "gammas": expected_gammas, "intensity": 1.0}
        assert Parser.parse(text) == expected

    def test_questionable_record(self):
        questionable = "208TL  G  576         0.001  LT                                                ?"
        normal = "208TL  G   39.857  4   2.96  24  M1                     23.2                 C  "

        assert Parser.questionable_record(questionable) == True
        assert Parser.questionable_record(normal) == False

    def test_is_alpha_decay_failure(self):
        header_record = "212PO    212BI B- DECAY (60.55 M)      1973DA38,1984GE07         20NDS    202009"
        assert Parser.is_alpha_decay(header_record) == False

    def test_is_alpha_decay_success(self):
        header_record = "208TL    212BI A DECAY (25.0 M)        1984ES01,1978BA44         07NDS    200707"
        assert Parser.is_alpha_decay(header_record) == True

    def test_is_ground_state_decay_failure(self):
        parent_record = "212BI  P  250         (9-)              25.0 M   2              6207.26   3"
        assert Parser.is_ground_state_decay(parent_record) == False

    def test_is_ground_state_decay_success(self):
        parent_record = "212BI  P 0.0          1(-)              60.55 M  6              6207.26   3"
        assert Parser.is_ground_state_decay(parent_record) == True
