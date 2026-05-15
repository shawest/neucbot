import pytest
import logging

from unittest import TestCase
from unittest.mock import call, patch

from neucbot import config


class TestConfig(TestCase):
    def setUp(self):
        self.raw_config = config.Config({"data_source": "talys-raw"})
        self.slim_config = config.Config({"data_source": "talys-slim"})

    @patch("shutil.which", return_value=True)
    def test_validate_no_talys_configured(self, mock_which):
        self.raw_config.validate()
        mock_which.assert_has_calls([])

    @patch("shutil.which", return_value=True)
    def test_validate_talys_configured_command_present(self, mock_which):
        cfg = self.raw_config
        cfg.talys = True
        cfg.validate()

        mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=True)
    def test_validate_force_recalc_with_talys_present(self, mock_which):
        cfg = self.raw_config
        cfg.force_recalculation = True
        cfg.validate()

        mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=False)
    def test_validate_talys_command_not_present(self, mock_which):
        with self.assertRaisesRegex(RuntimeError, r"talys command is not available"):
            cfg = self.raw_config
            cfg.talys = True
            cfg.validate()

            mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=True)
    def test_validate_slim_data_no_talys(self, mock_which):
        self.slim_config.validate()

        mock_which.assert_has_calls([])

    @patch("shutil.which", return_value=True)
    def test_validate_slim_data_with_talys_configured(self, mock_which):
        with self.assertRaisesRegex(
            RuntimeError, r"run TALYS calculations while using preprocessed data"
        ):
            cfg = self.slim_config
            cfg.talys = True
            cfg.validate()

            mock_which.assert_has_calls([])
