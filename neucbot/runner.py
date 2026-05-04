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

        condensed_alpha_list = alpha_list.condense(step_size)

        # If this is not being run as part of a web request, show a progress bar
        if not self.config.json:
            condensed_alpha_list = tqdm(condensed_alpha_list)

        for [energy, intensity] in condensed_alpha_list:
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

        outputs = {
            "total_neutron_yield": utils.format_float(total_cross_section),
            "cross_sections": {
                el: utils.format_float(x) for el, x in cross_sections.items()
            },
            "spectrum_integral": utils.format_float(
                utils.Histogram(spec_totals).integrate()
            ),
            "spectra_totals": {
                e: utils.format_float(v) for e, v in spec_totals.items()
            },
        }

        if self.config.json:
            return outputs
        else:
            self.print_outputs(outputs)
            return outputs

    def print_outputs(self, outputs):
        output_file = self.config.output

        print("", file=output_file)
        print(
            "# Total neutron yield = ",
            outputs["total_neutron_yield"],
            " n/decay",
            file=output_file,
        )

        cross_sections = outputs["cross_sections"]
        for x in sorted(cross_sections):
            print("\t", x, cross_sections[x], file=output_file)

        print(
            "# Integral of spectrum = ",
            outputs["spectrum_integral"],
            " n/decay",
            file=output_file,
        )

        spectra_totals = outputs["spectra_totals"]
        for e in sorted(spectra_totals):
            print(e, spectra_totals[e], file=output_file)
