import pytest

from unittest import TestCase
from unittest.mock import call, mock_open, patch

from neucbot import elements, material


class TestIsotope(TestCase):
    def setUp(self):
        carbon = elements.Element("C")
        self.isotope = material.Isotope(carbon, 13, 1.0)

    def test_material_term(self):
        assert self.isotope.material_term() == material.N_A * 1.0 / 13

    def test_name(self):
        assert self.isotope.name() == "C13"

    @patch(
        "neucbot.data.raw_talys.RawTalysDataSource.allows_talys_calculation",
        return_value=False,
    )
    def test_differential_n_spec_no_talys(self, mock_talys_allowed):
        pass

    @patch("neucbot.data.raw_talys.RawTalysDataSource.run_talys")
    @patch(
        "neucbot.data.raw_talys.RawTalysDataSource.allows_talys_calculation",
        return_value=True,
    )
    def test_differential_n_spec_force_recalculation(
        self, mock_talys_allowed, mock_talys
    ):
        self.isotope.differential_n_spec(1.05, False, True)
        mock_talys_allowed.assert_has_calls([call()])
        mock_talys.assert_has_calls([call(1.05)])

    @patch("neucbot.data.raw_talys.RawTalysDataSource.run_talys_with_retries")
    @patch(
        "neucbot.data.raw_talys.RawTalysDataSource.allows_talys_calculation",
        return_value=True,
    )
    def test_differential_n_spec_talys_allowed_and_run(
        self, mock_talys_allowed, mock_talys
    ):
        self.isotope.differential_n_spec(1.05, True)
        mock_talys_allowed.assert_has_calls([call()])
        mock_talys.assert_has_calls([call(1.05)])

    @patch(
        "neucbot.data.raw_talys.RawTalysDataSource.cross_section",
        return_value=1.51335e-28,
    )
    def test_cross_section(self, mock_cross_section):
        assert self.isotope.cross_section(1.05000002) == 1.51335e-28
        mock_cross_section.assert_has_calls([call(1.05)])


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

    def test_from_json(self):
        request_json = {
            "elements": [
                {"element": "C", "mass_number": "12", "fraction": "33"},
                {"element": "H", "mass_number": "1", "fraction": "33"},
                {"element": "O", "mass_number": "16", "fraction": "34"},
            ]
        }

        comp = material.Composition.from_json(request_json)

        assert len(comp.materials) == 3
        assert comp.fractions.get("C") == pytest.approx(0.33)
        assert comp.fractions.get("H") == pytest.approx(0.33)
        assert comp.fractions.get("O") == pytest.approx(0.34)

    def test_from_json_no_isotopes_specified(self):
        request_json = {
            "elements": [
                {"element": "C", "mass_number": "0", "fraction": "33"},
                {"element": "H", "mass_number": "0", "fraction": "33"},
                {"element": "O", "mass_number": "0", "fraction": "34"},
            ]
        }

        comp = material.Composition.from_json(request_json)

        assert len(comp.materials) == 7
        assert comp.fractions.get("C") == pytest.approx(0.33)
        assert comp.fractions.get("H") == pytest.approx(0.33)
        assert comp.fractions.get("O") == pytest.approx(0.34)

    def test_normalize(self):
        comp = material.Composition()

        comp.add({"element": "C", "mass_number": "12", "fraction": 0.4})
        comp.add({"element": "H", "mass_number": "1", "fraction": 0.2})
        comp.add({"element": "O", "mass_number": "16", "fraction": 0.2})

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

    @patch("subprocess.call")
    @patch("os.listdir", return_value=["data"])
    def test_download_data_all_data_present(self, mocked_listdir, mocked_call):
        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        comp.download_data("v2")

        mocked_listdir.assert_has_calls(
            [
                call("./Data/Isotopes/C/C12/TalysOut"),
                call("./Data/Isotopes/C/C12/NSpectra"),
                call("./Data/Isotopes/O/O16/TalysOut"),
                call("./Data/Isotopes/O/O16/NSpectra"),
                call("./Data/Isotopes/H/H1/TalysOut"),
                call("./Data/Isotopes/H/H1/NSpectra"),
            ]
        )

        mocked_call.assert_has_calls([])

    @patch("subprocess.call")
    @patch("os.listdir", return_value=[])
    def test_download_data_missing_data(self, mocked_listdir, mocked_call):
        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        comp.download_data("v2")

        mocked_listdir.assert_has_calls(
            [
                call("./Data/Isotopes/C/C12/TalysOut"),
                call("./Data/Isotopes/O/O16/TalysOut"),
                call("./Data/Isotopes/H/H1/TalysOut"),
            ]
        )

        mocked_call.assert_has_calls(
            [
                call("./Scripts/download_element_v2.sh C", shell=True),
                call("./Scripts/download_element_v2.sh O", shell=True),
                call("./Scripts/download_element_v2.sh H", shell=True),
            ]
        )


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
