import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot.data.raw_jendl import (
    RawJendlDataSource,
)


class TestRawJendlDataSource(TestCase):
    def setUp(self):
        # Patch calls to os.makedirs to make sure dirs aren't created
        makedirs_patcher = patch("os.makedirs")
        self.addCleanup(makedirs_patcher.stop)
        self.mock_makedirs = makedirs_patcher.start()

        with open("./tests/data/JendlOut/MT4/cross-section") as cross_sections_file:
            self.cross_sections_text = cross_sections_file.read()

        # Addtional helpers
        self.data_source = RawJendlDataSource("C", 13)
        self.data_source.base_dir = "./tests/data"
        self.data_source.output_dir = "./tests/data/JendlOut/MT4"

        with patch("builtins.open", mock_open(read_data=self.cross_sections_text)):
            self.data_source.set_cross_sections()

    # -------------------------------------------------------------
    # Tests for methods defined by NeucbotDataSource abstract class
    # -------------------------------------------------------------

    # RawJendlDataSource#cross_section
    def test_cross_section(self):
        expected_cross_sections = {
            0.0: 0.0,
            1.05: 9.537883333333333e-28,
            6.76: 1.9655826004430202e-25,
            6.77: 1.9864374503322648e-25,
            6.78: 2.00729230022151e-25,
            6.79: 2.0281471501107552e-25,
        }

        for alpha, cross_section in expected_cross_sections.items():
            assert self.data_source.cross_section(alpha) == pytest.approx(cross_section)

    def test_cross_section_non_exact_match(self):
        assert self.data_source.cross_section(6.775) == self.data_source.cross_section(
            6.77
        )

    @patch("builtins.hasattr", return_value=False)
    def test_cross_section_missing_cross_sections(self, mock_hasattr):
        assert self.data_source.cross_section(1.05) == 0.0

        mock_hasattr.assert_called()

    # RawJendlDataSource#nspectra
    @patch("os.path.exists", return_value=True)
    def test_nspectra(self, mock_exists):
        spectra = self.data_source.nspectra(1.05)

        assert len(spectra.to_dict().items()) == 150
        assert spectra.get(100) == 0.0
        assert spectra.get(2500) == pytest.approx(1.631442e-30)

    @patch("os.path.exists", return_value=False)
    def test_nspectra_missing_spectra_file(self, mock_exists):
        assert self.data_source.nspectra(1.05).to_dict() == {}

        mock_exists.assert_has_calls([call("./tests/data/JendlOut/MT4/outputE1.0500")])

    # RawJendlDataSource#download_data
    @patch.object(RawJendlDataSource, "set_cross_sections")
    @patch("subprocess.call")
    @patch("glob.glob", return_value=[])
    def test_download_data_no_existing_data(self, mock_glob, mock_call, mock_source):
        mock_call.assert_has_calls([])
        mock_source.assert_has_calls([])

    @patch.object(RawJendlDataSource, "set_cross_sections")
    @patch("subprocess.call")
    @patch("glob.glob", return_value=["some_dir"])
    def test_download_data_existing_data_found(self, mock_glob, mock_call, mock_source):
        mock_call.assert_has_calls([])
        mock_source.assert_has_calls([])

    # RawJendlDataSource#allows_talys_calculation
    def test_allows_talys_calculation(self):
        assert self.data_source.allows_talys_calculation() == False

    # ----------------------------------------
    # Tests for source-specific helper methods
    # ----------------------------------------
    # RawJendlDataSource#ensure_dirs_exist
    def test_ensure_dirs_exist(self):
        self.data_source.ensure_dirs_exist()

        self.mock_makedirs.assert_has_calls(
            [
                call(self.data_source.output_dir, exist_ok=True),
            ]
        )

    # RawJendlDataSource#output_file
    def test_output_file(self):
        assert (
            self.data_source.output_file(1.00)
            == f"{self.data_source.output_dir}/outputE1.0000"
        )

    # RawJendlDataSource#cross_section_file
    def test_cross_section_file(self):
        assert (
            self.data_source.cross_section_file()
            == f"{self.data_source.output_dir}/cross-section"
        )

    # RawJendlDataSource#set_cross_sections
    def test_set_cross_sections(self):
        assert hasattr(self.data_source, "cross_sections")
        assert len(self.data_source.cross_sections.items()) == 6

    @patch("os.path.exists", return_value=False)
    def test_set_cross_sections_no_file_found(self, mock_exists):
        data_source = RawJendlDataSource("C", 13)
        data_source.set_cross_sections()

        mock_exists.assert_has_calls(
            [
                call(data_source.cross_section_file()),
            ]
        )

        assert not hasattr(data_source, "cross_sections")
