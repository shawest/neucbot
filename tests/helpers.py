class MockDataSource:
    def __init__(self, element, mass_number):
        self.element = element
        self.mass_number = mass_number

    def allows_talys_calculation(self):
        return False

    def cross_section(self, rounded_alpha_energy):
        return 0

    def nspectra(self, rounded_alpha_energy):
        return {}

    def download_data(self, version):
        return

    def run_talys(self):
        return

    def run_talys_with_retries(self):
        return
