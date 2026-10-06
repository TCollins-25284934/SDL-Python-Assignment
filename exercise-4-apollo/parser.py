"""Flight Data parser

This script allows the user to parse flight data from a .txt file with a specific format.
The input file must follow the expected flight-data format i.e. comments and return characters
have a leading "$" character (and are ignored during parsing), comma separated table data with no leading characters, and
units in the row below the header row of table.

This script requires that 'numpy', 'matplotlib' be installed within the Python
environment you are running this script in. Plotting a coloured ground-track based on altitude is achieved using
the plot_colourline() function posted by Alejandro on Stack Overflow: https://stackoverflow.com/a/36521456.

A coloured ground-track plot is given by default, to output a non-coloured ground-track plot, the user must pass
--non_coloured True
after calling the script

Examples
-------
python parser.py as-505-ascent-phase-data.txt
python parser.py as-505-ascent-phase-data.txt --non_coloured True


"""

import csv
import argparse
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def parser(filename):
    """
    Parses flight data from a text file and generates plots for
    all recorded flight parameters.

    The function reads the input file, extracts the headers,
    units, and numerical data, and stores the results in NumPy
    arrays. It then produces:

        * Time-series plots for each flight variable against time.
        * A coloured ground-track plot where altitude determines
          the track colour (a non-coloured version if --non_coloured is specified True).

    Parameters
    ----------
    filename : str
        Path to the flight data file to be parsed.

    Returns
    -------
    None
        Displays the generated plots.
    """
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            table = [[entry.strip() for entry in row] for row in reader if all(entry[0] != "$" for entry in row)]

            headers = [row for row in table[0]]
            units = [row for row in table[1]]
            data = [[float(entry) for entry in row] for row in table[2:]]
    except FileNotFoundError:
        print(f"Error: '{filename}' could not be found.")
        return



    unit_dict = dict(zip(headers, units))

    nptable_dict = {header: np.array(column) for header, column in zip(headers, zip(*data))}
    plt.close('all')

    for key, values in nptable_dict.items():
        if key != "TIME":
            plt.plot(nptable_dict["TIME"], values,label=key)
            plt.xlabel("Time (s)")
            plt.ylabel(f"{key} ({unit_dict[key].lower()})")
            plt.legend()
            plt.grid(True)

            plt.show()

    map_path = Path(__file__).parent / "maps" / "NE1_50M_SR_W_CROPPED_1080.png"
    if args.non_coloured == False:
        lon = nptable_dict["LONG"]
        lat = nptable_dict["GC LAT"]
        alt = nptable_dict["ALTITUDE"]

        fig, ax = plt.subplots(figsize=(10, 8))

        im = plt.imread(map_path)
        ax.imshow(im, extent=[-120, -30, 15, 60])
        im = plot_colourline(lon, lat, alt)
        cbar = fig.colorbar(im)
        cbar.set_label("Altitude (km)")

        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Apollo 10 Ground Track")
        ax.set_aspect("equal")

        plt.show()
    else:
        # Non-coloured ground track
        fig, ax = plt.subplots()
        im = plt.imread(map_path)
        ax.imshow(im, extent=[-120,-30,15,60])
        plt.plot(nptable_dict["LONG"], nptable_dict["GC LAT"])
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Apollo 10 Ground Track")
        ax.set_aspect("equal")
        ax.set_aspect('equal')
        plt.show()

    return None



# Source - https://stackoverflow.com/a/36521456
# Posted by Alejandro, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-03, License - CC BY-SA 4.0
def plot_colourline(x,y,c):
    col = cm.jet((c-np.min(c))/(np.max(c)-np.min(c)))
    ax = plt.gca()
    for i in np.arange(len(x)-1):
        ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=col[i])
    im = ax.scatter(x, y, c=c, s=0, cmap=cm.jet)
    return im

def main(filename):
    parser(filename)

def parse_arguments():
    parser = argparse.ArgumentParser(description="""Flight Data Parser
                                                
                                                Reads flight telemetry data from a text file and produces:
                                                
                                                * Time-series plots of each recorded parameter.
                                                * A ground-track plot coloured by altitude (non-coloured by default).
                                                
                                                Examples
                                                -------
                                                python parser.py as-505-ascent-phase-data.txt
                                                python parser.py as-505-ascent-phase-data.txt --non_coloured True
                                                
                                                The input file must follow the expected flight-data format i.e comments
                                                and return characters have a leading "$" character, comma separated
                                                table data with no leading characters, and units in the row below the 
                                                header row of table.
                                                """)
    parser.add_argument('filename', help="flight data file")
    parser.add_argument('--non_coloured', type=bool, default=False, help = 'Will provide a non-coloured ground-track plot')
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()
    main(args.filename)
