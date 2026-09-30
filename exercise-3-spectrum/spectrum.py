import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename = 'spectrum.txt'

spec_dict = {}

# print(spec_dict.keys())
# def load_data(filename: str) -> dict:
#     with open(filename, 'r') as file:
#         reader = csv.DictReader(file, fieldnames=spec_dict.keys())
#         for row in reader:
#             # for key, value in row.items():
#             #     spec_dict[key].append(float(value))
#             pass
#     return spec_dict
# telemetry = load_data(filename)


lines = []
header = {}
wavelength = []
flux = []

with open("spectrum.txt", "r") as f:
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

#
def my_line(x, a, b,c,d):
    return a * x**3 + b*x**2 + c*x + d
# def my_line(x,a,b):
#     return a*x + b
# my_line = my_line(, 1, 2)
popt, pcov = curve_fit(
    my_line,
    wave,
    flux,

    )
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(wave, flux)
ax.plot(wave, my_line(wave, *popt), 'r--')
plt.show()

# def gaussian(x, A, mu, sigma, c):
#     return A * np.exp(-(x - mu)**2 / (2*sigma**2)) + c
# c0 = np.median(flux)
#
# A0 = np.max(flux) - c0
#
# mu0 = wave[np.argmax(flux)]
#
# sigma0 = 2.0
#
# p0 = [A0, mu0, sigma0, c0]
#
# popt, pcov = curve_fit(
#     gaussian,
#     wave,
#     flux,
#     p0=p0
# )
# fig, ax = plt.subplots(figsize=(10,10))
# ax.plot(wave, flux)
# ax.plot(wave, gaussian(wave, *popt), 'r--')
# plt.show()