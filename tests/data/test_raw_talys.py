import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot.data.raw_talys import (
    RawTalysDataSource,
    command_template,
    NEUTRON_CROSS_SECTION_PATTERN,
)


class TestRawTalysDataSource(TestCase):
    def setUp(self):
        # Patch calls to os.makedirs to make sure dirs aren't created
        makedirs_patcher = patch("os.makedirs")
        self.addCleanup(makedirs_patcher.stop)
        self.mock_makedirs = makedirs_patcher.start()

        # Populating data for nspectra tests
        with open("./tests/data/NSpectra/C13Nspec.txt") as nspec_file:
            self.nspec_text = nspec_file.read()

        self.expected_nspectra = {
            100: 4.11934e-33,
            200: 4.641829999999999e-33,
            300: 5.2085800000000005e-33,
            400: 5.819920000000001e-33,
            500: 6.47565e-33,
        }

        # Addtional helpers
        self.data_source = RawTalysDataSource("C", 13)
        self.expected_talys_call = "talys < ./Data/Isotopes/C/C13/TalysInputs/inputE1.0 > ./Data/Isotopes/C/C13/TalysOut/outputE1.0"
        self.expected_talys_params = command_template.substitute(
            element="C", mass_number=13, alpha_energy=1.00
        )

    # -------------------------------------------------------------
    # Tests for methods defined by NeucbotDataSource abstract class
    # -------------------------------------------------------------

    # RawTalysDataSource#cross_section
    @patch("os.path.exists", return_value=True)
    def test_cross_section(self, mock_exists):
        expected_cross_sections = {
            6.79: 3.40154e-25,
            6.78: 3.39437e-25,
            6.77: 3.38704e-25,
            6.76: 3.37965e-25,
            1.05: 1.51335e-28,
        }

        for alpha, cross_section in expected_cross_sections.items():
            with open(f"./tests/data/TalysOut/outputE{alpha}") as talys_out_file:
                talys_out_text = talys_out_file.read()
                with patch("builtins.open", mock_open(read_data=talys_out_text)):
                    assert self.data_source.cross_section(alpha) == cross_section

    @patch("os.path.exists", return_value=False)
    def test_cross_section_missing_talys_output_file(self, mock_exists):
        assert self.data_source.cross_section(5.00) == 0
        mock_exists.assert_has_calls(
            [call("./Data/Isotopes/C/C13/TalysOut/outputE5.0")]
        )

    @patch("re.search", return_value=None)
    @patch("os.path.exists", return_value=True)
    def test_cross_section_no_neutron_cross_section_match(
        self, mock_exists, mock_search
    ):
        mocked_open = mock_open(read_data="test_text")
        with patch("builtins.open", mocked_open):
            assert self.data_source.cross_section(7.77) == 0

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/TalysOut/outputE7.77", "r"),
                ]
            )

            mock_search.assert_has_calls(
                [call(NEUTRON_CROSS_SECTION_PATTERN, "test_text")]
            )

    # RawTalysDataSource#nspectra
    @patch("os.path.exists", return_value=True)
    def test_nspectra(self, mock_exists):
        mocked_open = mock_open(read_data=self.nspec_text)
        with patch("builtins.open", mocked_open):
            assert self.data_source.nspectra(1.0).to_dict() == self.expected_nspectra

            mock_exists.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

    @patch("os.path.exists", return_value=False)
    def test_nspectra_missing_spectra_file(self, mock_exists):
        assert self.data_source.nspectra(1.0).to_dict() == {}
        mock_exists.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
            ]
        )

    @patch("os.path.exists", return_value=True)
    def test_nspectra_empty_spectra_files(self, mock_exists):
        mocked_open = mock_open(read_data="EMPTY")
        with patch("builtins.open", mocked_open):
            assert self.data_source.nspectra(1.0).to_dict() == {}

            mock_exists.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

    # RawTalysDataSource#download_data
    @patch("subprocess.call")
    @patch("os.listdir", return_value=[])
    def test_download_data_no_existing_data(self, mock_listdir, mock_call):
        self.data_source.download_data()
        mock_call.assert_has_calls(
            [call("./Scripts/download_element_v2.sh C", shell=True)]
        )

    @patch("os.listdir", return_value=["talysout", "talysnspec"])
    def test_download_data_existing_data_found(self, mock_listdir):
        self.data_source.download_data()
        mock_listdir.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/TalysOut"),
                call("./Data/Isotopes/C/C13/NSpectra"),
            ]
        )

    # RawTalysDataSource#allows_talys_calculation
    def test_allows_talys_calculation(self):
        assert self.data_source.allows_talys_calculation() == True

    # ----------------------------------------
    # Tests for source-specific helper methods
    # ----------------------------------------
    # RawTalysDataSource#ensure_dirs_exist
    def test_ensure_dirs_exist(self):
        self.data_source.ensure_dirs_exist()

        self.mock_makedirs.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/TalysInputs", exist_ok=True),
                call("./Data/Isotopes/C/C13/TalysOut", exist_ok=True),
                call("./Data/Isotopes/C/C13/NSpectra", exist_ok=True),
            ]
        )

    # RawTalysDataSource#input_file
    def test_input_file(self):
        assert (
            self.data_source.input_file(1.00)
            == "./Data/Isotopes/C/C13/TalysInputs/inputE1.0"
        )

    # RawTalysDataSource#output_file
    def test_output_file(self):
        assert (
            self.data_source.output_file(1.00)
            == "./Data/Isotopes/C/C13/TalysOut/outputE1.0"
        )

    # RawTalysDataSource#spectra_file
    def test_spectra_file(self):
        assert (
            self.data_source.spectra_file(1.00)
            == "./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"
        )

    # RawTalysDataSource#run_talys
    @patch("os.replace")
    @patch("glob.glob", return_value=["nspec001.000.tot"])
    @patch("subprocess.call", return_value=0)
    def test_run_talys(self, mock_call, mock_glob, mock_replace):
        mocked_open = mock_open()

        with patch("builtins.open", mocked_open):
            self.data_source.run_talys(1.00)

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/TalysInputs/inputE1.0", "w"),
                    call().write(self.expected_talys_params),
                    call().close(),
                ]
            )

            mock_call.assert_has_calls([call(self.expected_talys_call, shell=True)])

            mock_glob.assert_has_calls([call(".*nspec.*")])

            mock_replace.assert_has_calls(
                [
                    call(
                        "nspec001.000.tot",
                        "./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot",
                    )
                ]
            )

    @patch("glob.glob")
    @patch("subprocess.call", return_value=0)
    def test_run_talys_empty_nspec_files(self, mock_call, mock_glob):
        mocked_open = mock_open()

        with patch("builtins.open", mocked_open):
            self.data_source.run_talys(1.00)

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/TalysInputs/inputE1.0", "w"),
                    call().write(self.expected_talys_params),
                    call().close(),
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot", "w"),
                    call().write("EMPTY"),
                    call().close(),
                ]
            )

            mock_call.assert_has_calls([call(self.expected_talys_call, shell=True)])

            mock_glob.assert_has_calls([call(".*nspec.*")])

    @patch("subprocess.call", return_value=1)
    def test_run_talys_command_failed(self, mock_call):
        mocked_open = mock_open()

        with patch("builtins.open", mocked_open):
            with self.assertRaisesRegex(RuntimeError, r"Failed TALYS command:"):
                self.data_source.run_talys(1.00)

    # RawTalysDataSource#run_talys_with_retries
    @patch("neucbot.data.raw_talys.RawTalysDataSource.run_talys")
    @patch("os.path.exists", return_value=False)
    def test_run_talys_with_retries(self, mock_exists, mock_run_talys):
        self.data_source.run_talys_with_retries(1.00)

        mock_exists.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
            ]
        )

        mock_run_talys.assert_has_calls([call(1.00), call(1.00), call(1.00)])
