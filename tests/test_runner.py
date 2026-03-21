import pytest

from unittest import TestCase
from unittest.mock import call, patch

import numpy

from neucbot import alpha, config, material, runner


class TestNeucbotRunner(TestCase):
    def test_run(self):
        cfg = config.Config({})
        neucbot = runner.NeucbotRunner(cfg)

        alpha_list = alpha.AlphaList.from_filepath("AlphaLists/Bi212Alphas.dat")
        alpha_list.load_or_fetch()

        comp = material.Composition.from_file("./tests/test_material/WithIsotopes.dat")

        expected = {
            "cross_sections": {
                "C12": numpy.float64(0.0),
                "H1": numpy.float64(0.0),
                "O16": numpy.float64(0.0),
            },
            "spectra_totals": {},
            "total_cross_section": numpy.float64(0.0),
        }

        assert neucbot.run(alpha_list, comp) == expected
