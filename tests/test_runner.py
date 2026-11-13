import pytest

from unittest import TestCase
from unittest.mock import call, patch

import numpy

from neucbot import alpha, config, material, runner, utils

from tests.helpers import MockDataSource


class TestNeucbotRunner(TestCase):
    @patch.object(material.Isotope, "cross_section", return_value=1e-27)
    @patch.object(utils.Histogram, "rebin", return_value=utils.Histogram({1000: 1}))
    @patch.object(
        material.Isotope, "differential_n_spec", return_value=utils.Histogram()
    )
    @patch.object(material.Composition, "stopping_power", return_value=100)
    def test_run(
        self, mocked_stop_power, mocked_diff_n_spec, mocked_rebin, mocked_cross_sect
    ):
        cfg = config.Config({})
        neucbot = runner.NeucbotRunner(cfg)

        alpha_list = alpha.AlphaList.from_filepath("AlphaLists/Bi212Alphas.dat")
        alpha_list.load_or_fetch()

        comp = material.Composition.from_file(
            "./tests/test_material/WithIsotopes.dat", MockDataSource
        )

        expected = {
            "cross_sections": {
                "C12": "1.52e-06",
                "H1": "9.10e-06",
                "O16": "5.69e-07",
            },
            "spectra_totals": {1000: "1.12e+22"},
            "spectrum_integral": "1.12e+25",
            "total_neutron_yield": "1.12e-05",
        }

        assert neucbot.run(alpha_list, comp) == expected

    @patch.object(alpha.AlphaList, "condense")
    @patch.object(material.Isotope, "cross_section", return_value=1e-27)
    @patch.object(utils.Histogram, "rebin", return_value=utils.Histogram({1000: 1}))
    @patch.object(
        material.Isotope, "differential_n_spec", return_value=utils.Histogram()
    )
    @patch.object(material.Composition, "stopping_power", return_value=100)
    def test_run_with_alpha_energy_loss(
        self,
        mocked_stop_power,
        mocked_diff_n_spec,
        mocked_rebin,
        mocked_cross_sect,
        mocked_condense,
    ):
        options = {"energy_loss": True}
        cfg = config.Config(options)
        neucbot = runner.NeucbotRunner(cfg)

        alpha_list = alpha.AlphaList.from_filepath("AlphaLists/Bi212Alphas.dat")
        alpha_list.load_or_fetch()

        comp = material.Composition.from_file(
            "./tests/test_material/WithIsotopes.dat", MockDataSource
        )

        expected = {
            "cross_sections": {
                "C12": "1.52e-06",
                "H1": "9.10e-06",
                "O16": "5.69e-07",
            },
            "probability_spectrum": {
                1000: "1.00e-03",
            },
            "spectra_totals": {1000: "1.12e+22"},
            "spectrum_integral": "1.12e+25",
            "total_neutron_yield": "1.12e-05",
        }

        results = neucbot.run(alpha_list, comp, options)

        assert results["cross_sections"] == expected["cross_sections"]
        assert results["spectra_totals"] == expected["spectra_totals"]
        assert results["spectrum_integral"] == expected["spectrum_integral"]
        assert results["total_neutron_yield"] == expected["total_neutron_yield"]
        assert results["probability_spectrum"] == expected["probability_spectrum"]

        assert isinstance(results["alpha_n_list"][1000], dict)
        assert isinstance(results["alpha_normed_probability_spectrum"][1000], dict)
        assert isinstance(results["alpha_probability_spectrum"][1000], dict)

        mocked_condense.assert_not_called()
