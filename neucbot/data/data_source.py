from abc import ABC, abstractmethod

from neucbot import utils


class NeucbotDataSource(ABC):
    def __init__(self, element, mass_number):
        self.element = element
        self.mass_number = mass_number

    @abstractmethod
    def cross_section(self) -> float:
        pass

    @abstractmethod
    def nspectra(self) -> utils.Histogram:
        pass

    @abstractmethod
    def download_data(self):
        pass

    @abstractmethod
    def allows_talys_calculation(self) -> bool:
        pass
