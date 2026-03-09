import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot.talys import command_template, Runner


@patch("os.makedirs")
class TestRunner(TestCase):

    @patch("os.replace")
    @patch("glob.glob", return_value=["nspec001.000.tot"])
    @patch("subprocess.call", return_value=0)
    def test_run_generated_nspec_files(
        self, mocked_subprocess_call, mocked_glob, mocked_replace, mocked_makedirs
    ):
        mocked_open = mock_open()
        with patch("builtins.open", mocked_open):
            runner = Runner("C", 12)
            runner.run(1.00)

            mocked_makedirs.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C12/TalysInputs", exist_ok=True),
                    call("./Data/Isotopes/C/C12/TalysOut", exist_ok=True),
                    call("./Data/Isotopes/C/C12/NSpectra", exist_ok=True),
                ]
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C12/TalysInputs/inputE1.0", "w"),
                    call().write(
                        command_template.substitute(
                            element="C", mass_number=12, alpha_energy=1.00
                        )
                    ),
                    call().close(),
                ]
            )

            mocked_subprocess_call.assert_has_calls(
                [
                    call(
                        "talys < ./Data/Isotopes/C/C12/TalysInputs/inputE1.0 > ./Data/Isotopes/C/C12/TalysOut/outputE1.0",
                        shell=True,
                    ),
                ]
            )

            mocked_glob.assert_has_calls([call(".*nspec.*")])

            mocked_replace.assert_has_calls(
                [
                    call(
                        "nspec001.000.tot",
                        "./Data/Isotopes/C/C12/NSpectra/nspec001.000.tot",
                    )
                ]
            )

    @patch("glob.glob")
    @patch("subprocess.call", return_value=0)
    def test_run_empty_nspec_files(
        self, mocked_subprocess_call, mocked_glob, mocked_makedirs
    ):
        mocked_open = mock_open()
        with patch("builtins.open", mocked_open):
            runner = Runner("C", 12)
            runner.run(1.00)

            mocked_makedirs.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C12/TalysInputs", exist_ok=True),
                    call("./Data/Isotopes/C/C12/TalysOut", exist_ok=True),
                    call("./Data/Isotopes/C/C12/NSpectra", exist_ok=True),
                ]
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C12/TalysInputs/inputE1.0", "w"),
                    call().write(
                        command_template.substitute(
                            element="C", mass_number=12, alpha_energy=1.00
                        )
                    ),
                    call().close(),
                    call("./Data/Isotopes/C/C12/NSpectra/nspec001.000.tot", "w"),
                    call().write("EMPTY"),
                    call().close(),
                ]
            )

            mocked_subprocess_call.assert_has_calls(
                [
                    call(
                        "talys < ./Data/Isotopes/C/C12/TalysInputs/inputE1.0 > ./Data/Isotopes/C/C12/TalysOut/outputE1.0",
                        shell=True,
                    ),
                ]
            )

            mocked_glob.assert_has_calls([call(".*nspec.*")])

    @patch("glob.glob")
    @patch("subprocess.call", return_value=1)
    def test_run_failed_talys(
        self, mocked_subprocess_call, mocked_glob, mocked_makedirs
    ):
        mocked_open = mock_open()
        with patch("builtins.open", mocked_open):
            runner = Runner("C", 12)

            with self.assertRaisesRegex(RuntimeError, r"Failed TALYS command:"):
                runner.run(1.00)
