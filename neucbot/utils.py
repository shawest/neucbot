import numpy

HISTO_MIN_BIN = 0  # keV
HISTO_MAX_BIN = 20000  # keV
HISTO_DELTA_BIN = 100  # keV


def format_float(number, precision=6):
    if number == 0:
        return "0.0"
    else:
        return numpy.format_float_scientific(number, precision=precision, unique=False)


def round_half_up(number):
    return int(number * 100.0 + 0.5) / 100.0


class Histogram:
    # Expects histo as a dict
    def __init__(self, histo={}):
        self.histo = histo

    def to_dict(self):
        return self.histo

    def keys(self):
        return list(self.histo.keys())

    def get(self, key):
        return self.histo[key]

    def integrate(self):
        integral = 0
        sorted_keys = sorted(self.histo)

        for i in sorted_keys:
            # Get the bin width
            if index := sorted_keys.index(i) > 0:
                delta = sorted_keys[index] - sorted_keys[index - 1]
            else:
                delta = sorted_keys[0]

            integral += self.histo[i] * delta
        return integral

    def rebin(self, step=HISTO_DELTA_BIN, min_bin=HISTO_MIN_BIN, max_bin=HISTO_MAX_BIN):
        bin_count = (max_bin - min_bin) / step
        rebinned = {}
        norms = {}
        sorted_histo = sorted(self.histo)

        for i in sorted_histo:
            index = sorted_histo.index(i)
            # Get the spacing between points
            delta = sorted_histo[0]
            if index > 0:
                delta = sorted_histo[index] - sorted_histo[index - 1]

            # If the x value is too low, put it in the underflow bin (-1)
            if i < min_bin:
                new_bin = -1
            # ...or the overflow bin if too high
            elif i > max_bin:
                new_bin = int(bin_count + 10 * step)
            # Otherwise, calculate the new bin
            else:
                new_bin = int(min_bin + int((i - min_bin) / step) * step)

            rebinned[new_bin] = rebinned.get(new_bin, 0) + self.histo[i] * delta
            norms[new_bin] = norms.get(new_bin, 0) + delta

        # Renormalize the new histogram
        for i in rebinned:
            if norms[i] > 0:
                rebinned[i] /= norms[i]

        return Histogram(rebinned)
