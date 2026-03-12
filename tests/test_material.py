import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot import elements, material
from neucbot.talys import Runner


class TestIsotope(TestCase):
    def setUp(self):
        carbon = elements.Element("C")
        self.isotope = material.Isotope(carbon, 13, 1.0)

        with open("./tests/test_material/C13Nspec.txt") as nspec_file:
            self.nspec_text = nspec_file.read()

        self.expected_nspec = {
            100: 4.11934e-33,
            200: 4.641829999999999e-33,
            300: 5.2085800000000005e-33,
            400: 5.819920000000001e-33,
            500: 6.47565e-33,
        }

    def test_material_term(self):
        assert self.isotope.material_term() == material.N_A * 1.0 / 13

    @patch.object(Runner, "run")
    @patch("os.path.exists", return_value=True)
    def test_differential_n_spec_file_exists(self, mocked_exists, mocked_talys_run):
        mocked_open = mock_open(read_data=self.nspec_text)
        with patch("builtins.open", mocked_open):
            assert self.isotope.differential_n_spec(1.0) == self.expected_nspec

            mocked_exists.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                    call("./Data/Isotopes/C/C13/TalysOut"),
                ]
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

    @patch("os.path.exists", return_value=False)
    def test_differential_n_spec_no_file_no_talys(self, mocked_exists):
        assert self.isotope.differential_n_spec(1.0, False) == {}
        mocked_exists.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
            ]
        )

    @patch.object(Runner, "run")
    @patch("os.path.exists")
    def test_differential_n_spec_no_file_run_talys(
        self, mocked_exists, mocked_talys_run
    ):
        mocked_exists.side_effect = [
            False,  # File doesn't exist initially
            False,  # Before first TALYS Run
            True,  # Found after first TALYS Run
            True,  # TALYS Output directory exists
        ]

        mocked_open = mock_open(read_data=self.nspec_text)
        with patch("builtins.open", mocked_open):
            assert self.isotope.differential_n_spec(1.0, True) == self.expected_nspec

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

            mocked_exists.assert_has_calls(
                [
                    # First check
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                    # Before successful TALYS run
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                    # After successful TALYS run
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                    call("./Data/Isotopes/C/C13/TalysOut"),
                ]
            )

    @patch.object(Runner, "run")
    @patch("os.path.exists", return_value=False)
    def test_differential_n_spec_no_file_run_talys_no_successful_retries(
        self, mocked_exists, mocked_talys_run
    ):
        assert self.isotope.differential_n_spec(1.0, True) == {}
        mocked_exists.assert_has_calls(
            [
                # First check
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                # Three failed attempts
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
            ]
        )

    @patch("os.path.exists")
    def test_differential_n_spec_no_output_dir(self, mocked_exists):
        mocked_exists.side_effect = [True, False]
        assert self.isotope.differential_n_spec(1.0) == {}

        mocked_exists.assert_has_calls(
            [
                call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                call("./Data/Isotopes/C/C13/TalysOut"),
            ]
        )

    @patch.object(Runner, "run")
    @patch("os.path.exists", return_value=True)
    def test_differential_n_spec_force_recalculation(
        self, mocked_exists, mocked_talys_run
    ):
        mocked_open = mock_open(read_data=self.nspec_text)
        with patch("builtins.open", mocked_open):
            assert (
                self.isotope.differential_n_spec(1.0, False, True)
                == self.expected_nspec
            )

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/NSpectra/nspec001.000.tot"),
                ]
            )

    @patch("os.path.exists", return_value=True)
    def test_cross_section_valid_file(self, mocked_exists):
        with open("./tests/test_material/TalysOut/outputE6.79") as talys_out_file:
            talys_out_text = talys_out_file.read()
            with patch("builtins.open", mock_open(read_data=talys_out_text)):
                assert self.isotope.cross_section(6.790000000000042) == 3.40154e-25

        with open("./tests/test_material/TalysOut/outputE6.78") as talys_out_file:
            talys_out_text = talys_out_file.read()
            with patch("builtins.open", mock_open(read_data=talys_out_text)):
                assert self.isotope.cross_section(6.780000000000042) == 3.39437e-25

        with open("./tests/test_material/TalysOut/outputE6.77") as talys_out_file:
            talys_out_text = talys_out_file.read()
            with patch("builtins.open", mock_open(read_data=talys_out_text)):
                assert self.isotope.cross_section(6.770000000000042) == 3.38704e-25

        with open("./tests/test_material/TalysOut/outputE6.76") as talys_out_file:
            talys_out_text = talys_out_file.read()
            with patch("builtins.open", mock_open(read_data=talys_out_text)):
                assert self.isotope.cross_section(6.760000000000042) == 3.37965e-25

        with open("./tests/test_material/TalysOut/outputE1.05") as talys_out_file:
            talys_out_text = talys_out_file.read()
            with patch("builtins.open", mock_open(read_data=talys_out_text)):
                assert self.isotope.cross_section(1.05) == 1.51335e-28

    @patch("re.search", return_value=None)
    @patch("os.path.exists", return_value=True)
    def test_cross_section_no_file_content_match(self, mocked_exists, mocked_search):
        mocked_open = mock_open(read_data=self.nspec_text)
        with patch("builtins.open", mocked_open):
            assert self.isotope.cross_section(7.77) == 0

            mocked_open.assert_has_calls(
                [
                    call("./Data/Isotopes/C/C13/TalysOut/outputE7.77", "r"),
                ]
            )

    @patch("os.path.exists", return_value=False)
    def test_cross_section_no_file_exists(self, mocked_exists):
        assert self.isotope.cross_section(5.55) == 0

        mocked_exists.assert_has_calls(
            [call("./Data/Isotopes/C/C13/TalysOut/outputE5.55")]
        )


class TestComposition(TestCase):
    def test_from_file_isotopes_specified(self):
        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        assert len(comp.materials) == 3
        assert comp.fractions.get("C") == pytest.approx(0.5)
        assert comp.fractions.get("H") == pytest.approx(0.25)
        assert comp.fractions.get("O") == pytest.approx(0.25)

    def test_from_file_no_isotopes_specified(self):
        comp = material.Composition.from_file("./tests/test_material/NoIsotopes.dat")

        assert len(comp.materials) == 7
        assert comp.fractions.get("C") == pytest.approx(0.5)
        assert comp.fractions.get("H") == pytest.approx(0.25)
        assert comp.fractions.get("O") == pytest.approx(0.25)

    def test_normalize(self):
        comp = material.Composition()

        comp.add(material.Isotope(elements.Element("C"), 12, 0.4))
        comp.add(material.Isotope(elements.Element("H"), 12, 0.2))
        comp.add(material.Isotope(elements.Element("O"), 12, 0.2))

        comp.normalize()

        assert comp.fractions.get("C") == pytest.approx(0.5)
        assert comp.fractions.get("H") == pytest.approx(0.25)
        assert comp.fractions.get("O") == pytest.approx(0.25)

    def test_stopping_power_single_element_material(self):
        comp = material.Composition.from_file("./tests/test_material/CarbonOnly.dat")
        assert len(comp.materials) == 1
        assert comp.fractions == {"C": 1.0}

        # Since this material is 100% carbon 12, stopping power is just computed
        # as the stopping power of carbon at this energy level
        assert comp.stopping_power(11.0) == 486.0835

    def test_stopping_power_multi_element_material(self):
        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        assert len(comp.materials) == 3
        assert comp.fractions.get("C") == pytest.approx(0.5)
        assert comp.fractions.get("H") == pytest.approx(0.25)
        assert comp.fractions.get("O") == pytest.approx(0.25)

        # 50% stopping power of C = 0.5 * 486.0835
        # 25% stopping power of H = 0.25 * 1371.204
        # 25% stopping power of O = 0.25 * 462.8758
        assert comp.stopping_power(11.0) == 701.5617


class TestStoppingPowerList(TestCase):
    def test_load_file(self):
        stop_list = material.StoppingPowerList("C")
        stop_list.load_file()

        assert len(stop_list.stopping_powers.items()) == 79
        assert stop_list.stopping_powers[0.01] == 511.72

    def test_for_alpha(self):
        stop_list = material.StoppingPowerList("C")
        stop_list.load_file()

        # Energy less than lowest energy in the list
        assert stop_list.for_alpha(0.001) == 511.72

        # Energies in between two entries in the list
        assert stop_list.for_alpha(0.525) == 1927.124
        assert stop_list.for_alpha(4.25) == 906.4551

        # Energy higher than the highest in the list
        assert stop_list.for_alpha(11.0) == 486.0835
