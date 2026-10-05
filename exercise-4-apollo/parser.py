"""Flight Data parser

This script allows the user to parse flight data from a .txt file with a specific format...

This script requires that `numpy`, 'argparse', 'csv', 'matplotlib' be installed within the Python
environment you are running this script in.
"""

import csv
import argparse
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np

def parser(filename):
    header_dict = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        # table = list(reader)
        print(reader)
        table = [[entry.strip() for entry in row] for row in reader if all(entry[0] !="$" for entry in row)]

        headers = [row for row in table[0]]
        units = [row for row in table[1]]
        data = [[float(entry) for entry in row] for row in table[2:]]

        header_dict = dict.fromkeys(headers)
        #
        # for row in data:
        #     # print(row)
        #     pass
        # table_dict = dict(zip(headers[0], data))
    # print(table_dict)
    # for i in zip(headers[0],data[0]):
    #     print(i)
    # for i in range(len(data)):
    #     table_dict = dict(zip(headers[0], data[i]))
    # print(table_dict)

    npdata = np.array(data)
    # print(npdata[0])
    # header_dict["TIME"] = npdata[:,0]
    # for i in zip(headers[0],npdata[:,0]):
    #     print(i)
    unit_dict = dict(zip(headers, units))
    # for key, value in unit_dict.items():
    #     print(key, value)

    nptable_dict = {header: np.array(column) for header, column in zip(headers, zip(*data))}
    plt.close('all')
    for key, values in nptable_dict.items():
        if key != "TIME":
            plt.plot(nptable_dict["TIME"], values,label=key)
            plt.xlabel("Time (s)")
            plt.ylabel(f"{key} ({unit_dict[key].lower()})")
            plt.legend()
            plt.show()

    # fig, ax = plt.subplots()
    # im = plt.imread("maps/NE1_50M_SR_W_CROPPED_1080.png")
    # ax.imshow(im, extent=[-120,-30,15,60])
    # plt.plot(nptable_dict["LONG"], nptable_dict["GC LAT"])
    #
    # ax.set_aspect('equal')
    # plt.show()


    lon = nptable_dict["LONG"]
    lat = nptable_dict["GC LAT"]
    alt = nptable_dict["ALTITUDE"]

    fig, ax = plt.subplots(figsize=(10, 8))

    im = plt.imread("maps/NE1_50M_SR_W_CROPPED_1080.png")
    ax.imshow(im, extent=[-120, -30, 15, 60])

    points = np.array([lon, lat]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)


    lc = LineCollection(segments, cmap="plasma")

    lc.set_array(alt[:-1])
    lc.set_linewidth(3)

    ax.add_collection(lc)

    # Add colour bar
    cbar = plt.colorbar(lc, ax=ax)
    cbar.set_label("Altitude (km)")

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Apollo 10 Ground Track")
    ax.set_aspect("equal")

    plt.show()

    return None




def main(filename):
    parser(filename)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Some description here')
    parser.add_argument('filename', help="flight data file")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()
    main(args.filename)
