from neucbot.data.data_source import NeucbotDataSource

class NeucbotDataSource(NeucbotDataSource):
    def __init__(self, element, mass_number):
        self.element = element
        self.mass_number = mass_number

    def cross_section(self):
        pass

    def nspectra(self):
        pass

    def download_data(self):
        pass

    def allows_talys_calculation(self):
        pass
