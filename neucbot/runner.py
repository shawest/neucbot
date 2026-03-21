from tqdm import tqdm
from neucbot import alpha
from neucbot import config
from neucbot import talys
from neucbot import utils

ALPHA_STEP = 0.01  # MeV


class NeucbotRunner:
    def __init__(self, cfg):
        self.config = cfg

    def run(self, alpha_list, material_composition, step_size=ALPHA_STEP):
        run_talys = self.config.talys
        force_recalc = self.config.force_recalculation
        print("Running alphas:")

        spec_totals = {}
        cross_sections = {}
        total_cross_section = 0

        for [energy, intensity] in tqdm(alpha_list.condense(step_size)):
            stopping_power = material_composition.stopping_power(energy)

            for material in material_composition.materials:
                mat_term = material.material_term()
                mat_name = material.name()

                # Get alpha n spectrum for this alpha and this target
                spec = material.differential_n_spec(
                    energy, run_talys, force_recalc
                ).rebin()

                # Add this spectrum to the total spectrum
                delta_ea = energy if step_size > energy else step_size
                prefactors = (intensity / 100.0) * mat_term * delta_ea / stopping_power
                xsect = prefactors * material.cross_section(energy)
                total_cross_section += xsect

                cross_sections[mat_name] = cross_sections.get(mat_name, 0) + xsect

                for e in spec.keys():
                    spec_totals[e] = spec_totals.get(e, 0) + prefactors * spec.get(e)

        self.print_outputs(total_cross_section, cross_sections, spec_totals)

        return {
            "total_cross_section": total_cross_section,
            "cross_sections": cross_sections,
            "spectra_totals": spec_totals,
        }

    def print_outputs(self, total_cross_section, cross_sections, spectra_totals):
        output_file = self.config.output

        rounded_total = utils.format_float(total_cross_section)
        rounded_integral = utils.format_float(
            utils.Histogram(spectra_totals).integrate()
        )

        print("", file=output_file)
        print("# Total neutron yield = ", rounded_total, " n/decay", file=output_file)

        for x in sorted(cross_sections):
            print("\t", x, utils.format_float(cross_sections[x]), file=output_file)

        print(
            "# Integral of spectrum = ", rounded_integral, " n/decay", file=output_file
        )

        for e in sorted(spectra_totals):
            print(e, utils.format_float(spectra_totals[e]), file=output_file)
