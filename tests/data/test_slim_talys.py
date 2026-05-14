import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot.data.slim_talys import (
    TalysSlimDataSource,
    TALYS_SLIM_URL,
    TALYS_SLIM_TAR_PATH,
)

ALPHA_TO_CROSS_SECTIONS = {
    "1.0": 9.15574e-29,
    "1.01": 1.01569e-28,
    "1.02": 1.12489e-28,
    "1.03": 1.24378e-28,
    "1.04": 1.3730300000000002e-28,
    "1.05": 1.51335e-28,
}

ALPHA_TO_NSPECTRA = {
    1.0: {
        100: 4.11934e-33,
        200: 4.641829999999999e-33,
        300: 5.2085800000000005e-33,
        400: 5.819920000000001e-33,
        500: 6.47565e-33,
    }
}


class TestTalysSlimDataSource(TestCase):
    def setUp(self):
        self.data_source = TalysSlimDataSource("C", 13)

    # -------------------------------------------------------------
    # Tests for methods defined by NeucbotDataSource abstract class
    # -------------------------------------------------------------

    # TalysSlimDataSource#cross_section
    @patch("json.load", return_value=ALPHA_TO_CROSS_SECTIONS)
    def test_cross_section(self, mock_load):
        with patch("builtins.open", mock_open()):
            for alpha, cross_section in ALPHA_TO_CROSS_SECTIONS.items():
                assert self.data_source.cross_section(alpha) == cross_section

    @patch("json.load", return_value={})
    def test_cross_section_energy_not_found(self, mock_load):
        with patch("builtins.open", mock_open()):
            assert self.data_source.cross_section(1.0) == 0

    # TalysSlimDataSource#nspectra
    @patch("json.load", return_value=ALPHA_TO_NSPECTRA)
    def test_nspectra(self, mock_load):
        with patch("builtins.open", mock_open()):
            assert self.data_source.nspectra(1.0).to_dict() == ALPHA_TO_NSPECTRA.get(
                1.0
            )

    @patch("json.load", return_value={})
    def test_nspectra_energy_not_found(self, mock_load):
        with patch("builtins.open", mock_open()):
            assert self.data_source.nspectra(1.0).to_dict() == {}

    # TalysSlimDataSource#download_data
    @patch("shutil.rmtree")
    @patch("os.remove")
    @patch("shutil.move")
    @patch("tarfile.TarFile.extractall")
    @patch("tarfile.open")
    @patch("requests.get")
    @patch("os.listdir", return_value=False)
    @patch("os.path.exists", return_value=True)
    def test_download_data_no_existing_data(
        self,
        mock_exists,
        mock_listdir,
        mock_get,
        mock_taropen,
        mock_extractall,
        mock_move,
        mock_remove,
        mock_rmtree,
    ):
        with patch("builtins.open", mock_open()):
            self.data_source.download_data()
            mock_exists.assert_has_calls([call("Data/TalysSlim")])
            mock_listdir.assert_has_calls([call("Data/TalysSlim")])
            mock_get.assert_has_calls([call(TALYS_SLIM_URL)])
            mock_taropen.assert_has_calls([call(TALYS_SLIM_TAR_PATH)])

    @patch("os.listdir", return_value=True)
    @patch("os.path.exists", return_value=True)
    def test_download_data_existing_data_found(self, mock_exists, mock_listdir):
        self.data_source.download_data()
        mock_exists.assert_has_calls([call("Data/TalysSlim")])
        mock_listdir.assert_has_calls([call("Data/TalysSlim")])

    # TalysSlimDataSource#allows_talys_calculation
    def test_allows_talys_calculation(self):
        assert self.data_source.allows_talys_calculation() == False

    # ----------------------------------------
    # Tests for source-specific helper methods
    # ----------------------------------------
    # TalysSlimDataSource#talys_outputs
    @patch("json.load", return_value=ALPHA_TO_CROSS_SECTIONS)
    def test_talys_outputs(self, mock_load):
        with patch("builtins.open", mock_open()):
            assert self.data_source.talys_outputs == ALPHA_TO_CROSS_SECTIONS

    # TalysSlimDataSource#talys_nspec
    @patch("json.load", return_value=ALPHA_TO_NSPECTRA)
    def test_talys_nspec(self, mock_load):
        with patch("builtins.open", mock_open()):
            assert self.data_source.talys_outputs == ALPHA_TO_NSPECTRA

    # TalysSlimDataSource#transform_keys
    def test_transform_keys(self):
        assert self.data_source.transform_keys(ALPHA_TO_CROSS_SECTIONS) == {
            1.0: 9.15574e-29,
            1.01: 1.01569e-28,
            1.02: 1.12489e-28,
            1.03: 1.24378e-28,
            1.04: 1.3730300000000002e-28,
            1.05: 1.51335e-28,
        }
