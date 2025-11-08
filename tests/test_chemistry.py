import pytest

from neucbot import chemistry

class TestChemistry:
    def test_getZ(self):
        assert chemistry.getZ("H") == 1
        assert chemistry.getZ("Si") == 14
        assert chemistry.getZ("Au") == 79

    def test_getElement(self):
        assert chemistry.getElement(1) == "H"
        assert chemistry.getElement(88) == "Ra"
        assert chemistry.getElement(118) == "Uuo"
        assert chemistry.getElement(1000) == "None"
