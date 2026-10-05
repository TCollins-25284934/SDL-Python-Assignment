"""Powertracker

This script will parse spectrum emission data from a .txt file and plot the flux versus wavlength. The script will then fit:
1. A third order polynomial continuum to the plot, excluding a 10 unit window around the peak flux
2. A gaussian function to the plot within a 10 unit window of the peak flux
3. The combined gaussian and continuum model over the whole dataset.
The script will output to the console the best fit parameters of the combined model.


"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

header = {}
def continuum(x, a, b, c, d):
    """Cubic polynomial continuum."""
    return a * x**3 + b * x**2 + c * x + d


def gaussian(x, A, mu, sigma):
    """Gaussian emission line."""
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))


def full_model(x, A, mu, sigma, a, b, c, d):
    """Continuum + Gaussian."""
    return continuum(x, a, b, c, d) + gaussian(x, A, mu, sigma)


def load_spectrum(filename):
    """

    """

    data = []
    lines = []

    wavelength = []
    flux = []
    with open(filename, "r") as f:
        contents = repr(f.read())
        # print(contents)
        line = contents[2:].split('#')
        for entry in line:
            lines.append(entry.strip())
        # print(lines)
        for item in lines:
            parts = item.strip().split('\\n')
            key = parts[0]
            value = '\n'.join(parts[1:])
            header[key] = value

    wavelngth = header['DATA'].split('\n')
    wavelngth.pop()
    for i, entry in enumerate(wavelngth):
        wavelngth[i] = entry.strip()
        wavelngth[i] = entry.replace("\"", "")
        # print(wavelngth[i])
        wavelngth[i] = entry.split(',')
        # print(entry)

    # print(wavelngth)
    wavelength = np.array(wavelngth)
    wave = wavelength[1:, 0].astype(float)
    flux = wavelength[1:, 1].astype(float)
    return wave, flux


def fit_continuum(wave, flux):
    """
    Fit polynomial while excluding the emission peak.
    """

    peak_index = np.argmax(flux)
    peak_wave = wave[peak_index]

    exclusion_width = 10

    mask = np.abs(wave - peak_wave) > exclusion_width

    popt, pcov = curve_fit(
        continuum,
        wave[mask],
        flux[mask]
    )

    return popt, pcov, mask


def fit_gaussian(wave, flux, continuum_params):
    """
    Fit Gaussian after subtracting continuum.
    """

    continuum_flux = continuum(wave, *continuum_params)

    residual_flux = flux - continuum_flux

    A0 = np.max(residual_flux)
    mu0 = wave[np.argmax(residual_flux)]
    sigma0 = 2.0

    popt, pcov = curve_fit(
        gaussian,
        wave,
        residual_flux,
        p0=[A0, mu0, sigma0]
    )

    return popt, pcov


def make_plots(wave, flux, continuum_params, gaussian_params, mask):

    continuum_fit = continuum(wave, *continuum_params)

    gaussian_fit = gaussian(wave, *gaussian_params)

    full_fit = continuum_fit + gaussian_fit

    # Plot 1
    plt.figure(figsize=(8, 5))
    plt.axvspan(
        wave[~mask].min(),
        wave[~mask].max(),
        color="grey",
        alpha=0.2,
        label="Emission Line Region (±10 units)"
    )
    plt.plot(wave, flux)
    plt.xlabel(f"Wavelength  ({header["WAVELENGTH UNIT"].strip()})")
    plt.ylabel(f"Flux ({header["FLUX UNIT"].strip()})")
    plt.title("Spectrum")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot 2
    plt.figure(figsize=(8, 5))
    plt.axvspan(
        wave[~mask].min(),
        wave[~mask].max(),
        color="grey",
        alpha=0.2,
        label="Emission Line Region (±10 units)"
    )
    plt.plot(wave, flux, label="Spectrum")
    plt.plot(
        wave,
        continuum_fit,
        "r--",
        label="Continuum"
    )
    plt.xlabel(f"Wavelength  ({header["WAVELENGTH UNIT"].strip()})")
    plt.ylabel(f"Flux ({header["FLUX UNIT"].strip()})")
    plt.legend()
    plt.title("Spectrum + Continuum")
    plt.grid(True)
    plt.show()

    # Plot 3
    plt.figure(figsize=(8, 5))
    plt.plot(wave, flux, label="Spectrum")
    plt.axvspan(
        wave[~mask].min(),
        wave[~mask].max(),
        color="grey",
        alpha=0.2,
        label="Emission Line Region (±10 units)"
    )
    plt.plot(
        wave,
        continuum_fit,
        "k--",
        label="Continuum"
    )
    plt.plot(
        wave,
        full_fit,
        "r-",
        label="Continuum + Gaussian"
    )
    plt.xlabel(f"Wavelength ({header["WAVELENGTH UNIT"].strip()})")
    plt.ylabel(f"Flux ({header["FLUX UNIT"].strip()})")
    plt.legend()
    plt.title("Spectrum + Continuum + Gaussian")
    plt.grid(True)
    plt.show()


def print_results(gaussian_params, gaussian_cov):
    errors = np.sqrt(np.diag(gaussian_cov))

    A, mu, sigma = gaussian_params

    A_err, mu_err, sigma_err = errors

    fwhm = 2.355 * sigma
    fwhm_err = 2.355 * sigma_err

    print("\nBest-fit Gaussian parameters")
    print("------------------------------------")
    print(f"Amplitude = {A:.4f} +/- {A_err:.4f}", {header["FLUX UNIT"]})
    print(f"Centre wavelength = {mu:.4f} +/- {mu_err:.4f} {header["WAVELENGTH UNIT"]}")
    print(f"Sigma = {sigma:.4f} +/- {sigma_err:.4f}")
    print(f"FWHM = {fwhm:.4f} +/- {fwhm_err:.4f}")


def main(filename):

    wave, flux = load_spectrum(filename)

    continuum_params, continuum_cov, mask = fit_continuum(
        wave,
        flux
    )

    gaussian_params, gaussian_cov = fit_gaussian(
        wave,
        flux,
        continuum_params
    )

    print_results(
        gaussian_params,
        gaussian_cov
    )

    make_plots(
        wave,
        flux,
        continuum_params,
        gaussian_params,
        mask
    )




if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filename",
        help="Spectrum file"
    )

    args = parser.parse_args()

    main(args.filename)