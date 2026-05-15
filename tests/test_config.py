import pytest
import logging

from unittest import TestCase
from unittest.mock import call, patch

from neucbot import config


class TestConfig(TestCase):
    @patch("shutil.which", return_value=True)
    def test_validate_no_talys_configured(self, mock_which):
        config.Config({"talys": False}).validate()
        mock_which.assert_has_calls([])

    @patch("shutil.which", return_value=True)
    def test_validate_talys_configured_command_present(self, mock_which):
        config.Config({"talys": True}).validate()
        mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=True)
    def test_validate_talys_configured_command_present_force_recalc_passed(
        self, mock_which
    ):
        config.Config({"force_recalculation": True}).validate()
        mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=False)
    def test_validate_talys_configured_command_not_present(self, mock_which):
        with self.assertRaisesRegex(RuntimeError, r"talys command is not available"):
            config.Config({"talys": True}).validate()
            mock_which.assert_has_calls([call("talys")])

    @patch("shutil.which", return_value=True)
    def test_validate_slim_data_no_talys(self, mock_which):
        config.Config({"talys": False, "data_source": "slim"}).validate()
        mock_which.assert_has_calls([])

    @patch("shutil.which", return_value=True)
    def test_validate_slim_data_with_talys_configured(self, mock_which):
        with self.assertRaisesRegex(
            RuntimeError, r"run TALYS while using preprocessed data"
        ):
            config.Config({"talys": True, "data_source": "slim"}).validate()
            mock_which.assert_has_calls([])
