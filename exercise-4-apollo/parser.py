import csv
import numpy as np
import matplotlib.pyplot as plt

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

    return None




def main():
    parser("as-505-ascent-phase-data.txt")
main()