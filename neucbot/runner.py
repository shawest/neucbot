import numpy

from collections import defaultdict

from tqdm import tqdm
from neucbot import alpha
from neucbot import config
from neucbot import utils


class NeucbotRunner:
    def __init__(self, cfg):
        self.config = cfg

    def run(self, alpha_list, material_composition, options={}):
        if options.get("energy_loss"):
            return self._run_with_energy_loss(alpha_list, material_composition)
        else:
            return self._run_without_energy_loss(alpha_list, material_composition)

    def _run_without_energy_loss(self, alpha_list, material_composition):
        spec_totals = {}
        cross_sections = {}
        total_cross_section = 0

        condensed_alpha_list = alpha_list.condense(self.config.step_size)

        # If this is not being run as part of a web request, show a progress bar
        if not self.config.json:
            print("Running alphas:")
            condensed_alpha_list = tqdm(condensed_alpha_list)

        for [energy, intensity] in condensed_alpha_list:
            stopping_power = material_composition.stopping_power(energy)

            for material in material_composition.materials:
                mat_term = material.material_term()
                mat_name = material.name()

                # Get alpha n spectrum for this alpha and this target
                spec = material.differential_n_spec(
                    energy, self.config.talys, self.config.force_recalculation
                ).rebin()

                # Add this spectrum to the total spectrum
                delta_ea = (
                    energy if self.config.step_size > energy else self.config.step_size
                )
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

        return self.print_outputs(outputs)

    def _run_with_energy_loss(self, alpha_list, material_composition):
        cross_sections = {}
        spec_totals = {}
        total_cross_section = 0

        # Variables specific to the energy loss calculation
        probability_spec_totals = {}
        alpha_n_spec = {}
        alpha_n_probability_spec = {}
        alpha_n_normed_probability_spec = {}

        alpha_energy_steps = alpha_list.alpha_steps(self.config.step_size)
        max_alpha = alpha_energy_steps[0]

        precomputed = self.precompute_energy_step_values(
            alpha_energy_steps, material_composition
        )

        for [alpha_energy, intensity] in tqdm(alpha_list.alphas):
            rounded_alpha_energy = utils.round_half_up(alpha_energy)
            scaled_intensity = intensity / 100.0

            for energy in alpha_energy_steps:
                # Only start counting for steps at or below this alpha_energy
                if rounded_alpha_energy != max_alpha and energy >= rounded_alpha_energy:
                    continue

                delta = round(alpha_energy - energy, 2)

                for material in material_composition.materials:
                    mat_name = material.name()

                    xsect = (
                        scaled_intensity
                        * precomputed["cross_sections"][mat_name][energy]
                    )
                    total_cross_section += xsect

                    cross_sections[mat_name] = cross_sections.get(mat_name, 0) + xsect

                for e, value in precomputed["spectra"][energy].items():
                    energy_spec = scaled_intensity * value
                    spec_totals[e] = spec_totals.get(e, 0) + energy_spec
                    alpha_n_spec[e] = alpha_n_spec.get(e, {})
                    alpha_n_spec[e][delta] = alpha_n_spec[e].get(delta, 0) + energy_spec

        spectrum_integral = utils.Histogram(spec_totals).integrate()

        for energy in spec_totals.keys():
            total = spec_totals.get(energy)
            probability_spec_totals[energy] = total / spectrum_integral

            if total == 0:
                continue

            alpha_n_delta_map = alpha_n_spec.get(energy)

            for delta, spec in alpha_n_delta_map.items():
                prob_spec = alpha_n_probability_spec.get(energy, {})
                prob_spec[delta] = spec / total
                alpha_n_probability_spec[energy] = prob_spec

                norm_prob_spec = alpha_n_normed_probability_spec.get(energy, {})
                norm_prob_spec[delta] = spec / spectrum_integral
                alpha_n_normed_probability_spec[energy] = norm_prob_spec

        alpha_n_list = {}
        for energy in spec_totals.keys():
            total = spec_totals.get(energy)

            if total == 0:
                continue

            alpha_n_graph = {}

            for delta, spec in alpha_n_spec.get(energy).items():
                alpha_n_graph[delta] = spec / utils.HISTO_DELTA_BIN

            alpha_n_list[energy] = alpha_n_graph

        outputs = {
            "total_neutron_yield": utils.format_float(total_cross_section),
            "alpha_probability_spectrum": alpha_n_probability_spec,
            "alpha_normed_probability_spectrum": alpha_n_normed_probability_spec,
            "alpha_n_list": alpha_n_list,
            "cross_sections": {
                el: utils.format_float(x) for el, x in cross_sections.items()
            },
            "probability_spectrum": {
                e: utils.format_float(v) for e, v in probability_spec_totals.items()
            },
            "spectrum_integral": utils.format_float(spectrum_integral),
            "spectra_totals": {
                e: utils.format_float(v) for e, v in spec_totals.items()
            },
        }

        return self.print_outputs(outputs)

    def precompute_energy_step_values(self, alpha_energy_steps, material_composition):
        cross_sections = defaultdict(dict)
        spectra = {}

        for energy in alpha_energy_steps:
            stopping_power = material_composition.stopping_power(energy)
            delta = energy if self.config.step_size > energy else self.config.step_size

            energy_step_spectra = defaultdict(float)

            for material in material_composition.materials:
                mat_term = material.material_term()
                mat_name = material.name()

                prefactor = mat_term * delta / stopping_power
                spec = material.differential_n_spec(
                    energy, self.config.talys, self.config.force_recalculation
                ).rebin()

                for e, value in spec.items():
                    energy_step_spectra[e] += prefactor * value

                cross_sections[mat_name][energy] = prefactor * material.cross_section(
                    energy
                )

            spectra[energy] = dict(energy_step_spectra)

        return {
            "cross_sections": dict(
                cross_sections
            ),  # These do not have per-alpha intensities
            "spectra": dict(spectra),
        }

    def print_outputs(self, outputs):
        # Return early without printing outputs if this is in a web context
        if self.config.json:
            return outputs

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

        return outputs
