import argparse

def generate_list(end_number, Compword_list, Factor_list):
    for i in range(1, end_number+1):
        print(check_number(i, Compword_list, Factor_list))

def split_string(given_str):
    a, b = given_str[:len(given_str)// 2], given_str[len(given_str)// 2:]
    return a, b

def split_string_list(CompWord_list):
    starts = []
    ends = []
    for CompWord in CompWord_list:
        starts.append(split_string(CompWord)[0])
        ends.append(split_string(CompWord)[1])
    return starts, ends

def check_number(number,CompWord_list, intuple_list):
    starts, ends = split_string_list(CompWord_list)
    dct = dict(intuple_list)

    for i,j in enumerate(dct.keys()):
        if number % j == 0 and number % dct[j]== 0:
            return CompWord_list[i]

        elif number % j == 0:
            return starts[i]

        elif number % dct[j] == 0:
            return ends[i]

    else:
        return number

def main(end_number, Word_list, Factor_list):
    generate_list(end_number, Factor_list, Word_list)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Some description here')
    parser.add_argument('end_number', type=int, help="The length of teh list you'd like to print, must be an integer value")
    parser.add_argument('--Factor_list', type=list, help = "A list of factor tuples, a printed number whose divisor is contained within this list will be substituted for the paired compound word in Word_list",)
    parser.add_argument('--Word_list', type = list, help = "An optional list of compound words that will be paired with the factor list, must have the same length as the Factor List")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.end_number, args.Factor_list, args.Word_list)


