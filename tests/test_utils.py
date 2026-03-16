import pytest
from unittest import TestCase

from neucbot import utils


class TestUtils(TestCase):
    def test_format_float_zero(self):
        assert utils.format_float(0) == "0.0"
        assert utils.format_float(0.0) == "0.0"
        assert utils.format_float(0.0e0) == "0.0"

    def test_format_float_nonzero(self):
        assert utils.format_float(0.123456789) == "1.234568e-01"
        assert utils.format_float(1.987654321e10) == "1.987654e+10"

    def test_format_float_allows_precision(self):
        assert utils.format_float(0.123456789, 3) == "1.235e-01"
        assert utils.format_float(12345678991, 9) == "1.234567899e+10"


class TestHistogram(TestCase):
    def setUp(self):
        self.histogram = utils.Histogram(
            {
                100: 1,
                200: 2,
                300: 3,
                400: 4,
                500: 5,
            }
        )

    def test_get(self):
        assert self.histogram.get(200) == 2
        assert self.histogram.get(300) == 3
        assert self.histogram.get(400) == 4

    def test_keys(self):
        assert self.histogram.keys() == [100, 200, 300, 400, 500]

    def test_integrate(self):
        assert self.histogram.integrate() == 1500

    def test_to_dict(self):
        assert self.histogram.to_dict() == {
            100: 1,
            200: 2,
            300: 3,
            400: 4,
            500: 5,
        }

    def test_rebin(self):
        assert self.histogram.rebin().to_dict() == self.histogram.to_dict()
