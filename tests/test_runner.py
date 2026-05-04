import pytest

from unittest import TestCase
from unittest.mock import call, patch

import numpy

from neucbot import alpha, config, material, runner, utils


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

        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        expected = {
            "cross_sections": {
                "C12": "1.517499e-06",
                "H1": "9.104992e-06",
                "O16": "5.690620e-07",
            },
            "spectra_totals": {1000: "1.119155e+22"},
            "spectrum_integral": "1.119155e+25",
            "total_neutron_yield": "1.119155e-05",
        }

        assert neucbot.run(alpha_list, comp) == expected
