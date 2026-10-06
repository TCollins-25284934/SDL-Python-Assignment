"""Spectrum emission fitter and plotter

This script will parse spectrum emission data from a .txt file and plot the flux versus wavelength. The script will then fit:
1. A third order polynomial continuum to the plot, excluding a 10 unit window around the peak flux
2. A gaussian function to the plot within a 10 unit window of the peak flux
3. The combined gaussian and continuum model over the whole dataset.
The script will output to the console the best fit parameters of the combined model.

Microsoft Co-pilot was used to draft docstrings and headers, along with brainstorming for plotting and fitting


"""
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

header = {}
def continuum(x, a, b, c, d):
    """
    Evaluates a third-order polynomial continuum model.

    The continuum model is used to represent the baseline
    spectrum outside the emission-line region.

    Parameters
    ----------
    x : np.ndarray
        Wavelength values at which to evaluate the continuum.

    a : float
        Cubic coefficient.

    b : float
        Quadratic coefficient.

    c : float
        Linear coefficient.

    d : float
        Constant coefficient.

    Returns
    -------
    np.ndarray
        Continuum flux values
    """
    return a * x**3 + b * x**2 + c * x + d


def gaussian(x, A, mu, sigma):
    """
    Evaluates a Gaussian emission-line model.

    Parameters
    ----------
    x : np.ndarray
        Wavelength values at which to evaluate the Gaussian.

    A : float
        Amplitude of the emission line.

    mu : float
        Central wavelength of the emission line.

    sigma : float
        Standard deviation of the Gaussian.

    Returns
    -------
    np.ndarray
        Gaussian flux values evaluated at x.
    """
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))


def full_model(x, A, mu, sigma, a, b, c, d):
    """
    Evaluates the combined continuum and Gaussian model.

    The model consists of a third-order polynomial continuum
    and a Gaussian emission line.

    Parameters
    ----------
    x : np.ndarray
        Wavelength values at which to evaluate the model.

    A : float
        Amplitude of the Gaussian emission line.

    mu : float
        Central wavelength of the Gaussian emission line.

    sigma : float
        Standard deviation of the Gaussian.

    a : float
        Cubic continuum coefficient.

    b : float
        Quadratic continuum coefficient.

    c : float
        Linear continuum coefficient.

    d : float
        Constant continuum coefficient.

    Returns
    -------
    np.ndarray
        Combined model evaluated at x.
    """
    return continuum(x, a, b, c, d) + gaussian(x, A, mu, sigma)


def read_spectrum(filename):
    """
    Loads wavelength and flux data from a .txt file.

    The input file is expected to contain headers separated with a leading '#'
    and a DATA section containing comma-
    separated wavelength and flux values.
    Rows containing data do not have leading characters.

    Parameters
    ----------
    filename : str
        Path to the data file.

    Returns
    -------
    wave : np.ndarray
        Array of wavelength values.

    flux : np.ndarray
        Array of flux values.
    """
    lines = []
    try:
        with open(filename, "r") as f:
            contents = repr(f.read())
            line = contents[2:].split('#')
            for entry in line:
                lines.append(entry.strip())
            for item in lines:
                parts = item.strip().split('\\n')
                key = parts[0]
                value = '\n'.join(parts[1:])
                header[key] = value
    except FileNotFoundError:
        print(f"Error: '{filename}' could not be found.")
        return None, None


    wavelength = header['DATA'].split('\n')
    wavelength.pop()
    for i, entry in enumerate(wavelength):
        wavelength[i] = entry.strip()
        wavelength[i] = entry.replace("\"", "")
        wavelength[i] = entry.split(',')
    wavelength = np.array(wavelength)
    wave = wavelength[1:, 0].astype(float)
    flux = wavelength[1:, 1].astype(float)
    return wave, flux


def fit_continuum(wave, flux):
    """
    Fit a cubic polynomial while excluding the emission peak

    A region extending ±10 wavelength units around the peak
    emission is excluded from the fit to prevent the emission
    line from influencing the continuum model.

    Parameters
    ----------
    wave : np.ndarray
        Wavelength values.

    flux : np.ndarray
        Measured flux values.

    Returns
    -------
    popt : np.ndarray
        Best-fit continuum parameters.

    pcov : np.ndarray
        Covariance matrix of the continuum fit.

    mask : np.ndarray
        Boolean mask indicating the wavelength values
        included in the continuum fit.
    """

    peak_index = np.argmax(flux)
    peak_wave = wave[peak_index]

    exclusion_width = 10

    mask = np.abs(wave - peak_wave) > exclusion_width
    try:
        popt, pcov = curve_fit(continuum, wave[mask], flux[mask])
    except RuntimeError:
        print("Error: Fit failed to converge.")
        return None, None


    return popt, pcov, mask


def fit_gaussian(wave, flux, continuum_params):
    """
    Fits a Gaussian model to the 10 unit area around the emission peak.

    Parameters
    ----------
    wave : np.ndarray
        Wavelength values.

    flux : np.ndarray
        Measured flux values.

    continuum_params : np.ndarray
        Best-fit parameters from the continuum fit.

    Returns
    -------
    popt : np.ndarray
        Best-fit Gaussian parameters.

    pcov : np.ndarray
        Covariance matrix of the Gaussian fit.
    """

    continuum_flux = continuum(wave, *continuum_params)

    residual_flux = flux - continuum_flux

    A0 = np.max(residual_flux)
    mu0 = wave[np.argmax(residual_flux)]

    mask = residual_flux > A0 / 2

    fwhm = wave[mask].max() - wave[mask].min()

    sigma0 = fwhm / 2.355
    try:
        popt, pcov = curve_fit(gaussian, wave, residual_flux, p0=[A0, mu0, sigma0])
    except RuntimeError:
        print("Error: Fit failed to converge.")
        return None, None

    return popt, pcov

def fit_full_model(wave, flux, continuum_params, gaussian_params):
    """
    Fits continuum and Gaussian simultaneously.

    Continuum and Gaussian parameters obtained from previous
    fitting steps are used as initial parameter estimates.
    The full model is then fitted to the entire spectrum.

    Parameters
    ----------
    wave : np.ndarray
        Wavelength values.

    flux : np.ndarray
        Measured flux values.

    continuum_params : np.ndarray
        Best-fit continuum parameters.

    gaussian_params : np.ndarray
        Best-fit Gaussian parameters.

    Returns
    -------
    popt : np.ndarray
        Best-fit parameters of the combined model.

    pcov : np.ndarray
        Covariance matrix of the combined model fit.
    """

    A0, mu0, sigma0 = gaussian_params
    a0, b0, c0, d0 = continuum_params

    p0 = [
        A0,
        mu0,
        sigma0,
        a0,
        b0,
        c0,
        d0
    ]


    try:
        popt, pcov = curve_fit(full_model, wave, flux, p0=p0)
    except RuntimeError:
        print("Error: Fit failed to converge.")
        return None, None

    return popt, pcov


def make_plots(wave, flux, full_params, mask):
    """
    Generates plots showing the spectrum and fitted models.

    Three plots are produced:

        * Spectrum only.
        * Spectrum with fitted continuum.
        * Spectrum with fitted continuum and full model.

    Parameters
    ----------
    wave : np.ndarray
        Wavelength values.

    flux : np.ndarray
        Measured flux values.

    full_params : np.ndarray
        Best-fit parameters of the combined model.

    mask : np.ndarray
        Boolean mask of the spectrum excluding 10 units around teh emission peak.

    Returns
    -------
    None
        Displays the plots.
    """
    A, mu, sigma, a, b, c, d = full_params

    continuum_fit = continuum(wave, a, b, c, d)

    # gaussian_fit = gaussian(wave, A, mu, sigma)

    full_fit = full_model(wave, *full_params)

    wave_unit = header["WAVELENGTH UNIT"].strip()
    flux_unit = header["FLUX UNIT"].strip()

    # Plot 1
    plt.figure(figsize=(8, 5))
    plt.axvspan(wave[~mask].min(), wave[~mask].max(), color="grey", alpha=0.2, label="Emission Line Region (±10 units)")
    plt.plot(wave, flux)
    plt.xlabel(f"Wavelength ({wave_unit})")
    plt.ylabel(f"Flux ({flux_unit})")
    plt.title("Spectrum")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot 2
    plt.figure(figsize=(8, 5))
    plt.axvspan(wave[~mask].min(), wave[~mask].max(), color="grey", alpha=0.2, label="Emission Line Region (±10 units)")
    plt.plot(wave, flux, label="Spectrum")
    plt.plot(wave, continuum_fit, "r--", label="Continuum")
    plt.xlabel(f"Wavelength ({wave_unit})")
    plt.ylabel(f"Flux ({flux_unit})")
    plt.title("Spectrum + Continuum")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot 3
    plt.figure(figsize=(8, 5))
    plt.axvspan(wave[~mask].min(), wave[~mask].max(), color="grey", alpha=0.2, label="Emission Line Region (±10 units)")
    plt.plot(wave, flux, label="Spectrum")
    plt.plot(wave, continuum_fit, "k--", label="Continuum")
    plt.plot(wave, full_fit, "r-", label="Full Model")
    plt.xlabel(f"Wavelength ({wave_unit})")
    plt.ylabel(f"Flux ({flux_unit})")
    plt.title("Spectrum + Continuum + Gaussian")
    plt.legend()
    plt.grid(True)
    plt.show()


def print_results(full_params, full_cov):
    """
    Prints the best-fit model parameters and uncertainties.

    The function outputs the Gaussian amplitude, centre,
    sigma, full-width at half maximum (FWHM), and all
    continuum coefficients with their
    uncertainties.

    Parameters
    ----------
    full_params : np.ndarray
        Best-fit parameters of the combined model.

    full_cov : np.ndarray
        Covariance matrix returned by the combined model fit.

    Returns
    -------
    None
        Prints parameter estimates to the console.
    """
    errors = np.sqrt(np.diag(full_cov))

    A, mu, sigma, a, b, c, d = full_params

    A_err, mu_err, sigma_err, a_err, b_err, c_err, d_err = errors

    wave_unit = header["WAVELENGTH UNIT"].strip()
    flux_unit = header["FLUX UNIT"].strip()

    fwhm = 2.355 * sigma
    fwhm_err = 2.355 * sigma_err

    print("\nBest-fit Full Model Parameters")
    print("------------------------------------")

    print(f"Amplitude = {A:.4f} +/- {A_err:.4f} {flux_unit}")

    print(f"Centre wavelength = {mu:.4f} +/- {mu_err:.4f} {wave_unit}")

    print(f"Sigma = {sigma:.4f} +/- {sigma_err:.4f} {wave_unit}")

    print(f"FWHM = {fwhm:.4f} +/- {fwhm_err:.4f} {wave_unit}")

    print("\nContinuum Parameters")
    print(f"a = {a:.4e} +/- {a_err:.4e}")
    print(f"b = {b:.4e} +/- {b_err:.4e}")
    print(f"c = {c:.4e} +/- {c_err:.4e}")
    print(f"d = {d:.4e} +/- {d_err:.4e}")
def main(filename):

    wave, flux = read_spectrum(filename)

    continuum_params, continuum_cov, mask = fit_continuum(wave, flux)

    gaussian_params, gaussian_cov = fit_gaussian(wave, flux, continuum_params)
    full_params, full_cov = fit_full_model(wave, flux, continuum_params, gaussian_params)

    make_plots(wave, flux, full_params, mask)

    print_results(full_params, full_cov)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("filename", help="Spectrum file")
    args = parser.parse_args()
    main(args.filename)