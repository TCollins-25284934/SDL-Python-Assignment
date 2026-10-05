"""FizzBuzz game

Fizzbuzz is a mathematical game used to help kids learn their times tables. In
the game, a group of people will count up from 1, replacing any multiples of
3 by "Fizz" and any multiples of 5 by "Buzz". Numbers, such as 15,
which are multiples of both 3 and 5 are replaced by "FizzBuzz" in the
counting sequence.

This script allows a user to input the desired length of the counting sequence, as well as the number of
compound words and factor pairs. By default, with no inputs, the script will output the traditional FizzBuzz format with factors of 3 and 5.

This file can also be imported as a module and contains the following
functions:

    * split_string - Splits a string in half, in the case of uneven strings will front load the first half
    * split_string_list - Splits a list of strings in half using the split_string function
    * check_number - Checks whether a number is a multiple of any factor in an inputted list, and if so, pairs it with the corresponding half of a compound word from an inputted list
    * main - the main function of the script
"""
import argparse

def generate_list(end_number, Factor_list, Compword_list):
    print(Compword_list)
    print(Factor_list)
    for i in range(1, end_number+1):
        print(check_number(i, Factor_list, Compword_list))

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

def check_number(number, intuple_list, CompWord_list):
    starts, ends = split_string_list(CompWord_list)
    factor_pairs = list(zip(intuple_list[::2], intuple_list[1::2]))
    dct = dict(zip(factor_pairs, CompWord_list))
    result = ""

    for i, ((a, b), word) in enumerate(dct.items()):

        if number % a == 0 and number % b == 0:
            result += word

        elif number % a == 0:
            result += starts[i]

        elif number % b == 0:
            result += ends[i]

    if result == "":
        result = number

    return result

def main(end_number, factors, Word_list):
    generate_list(end_number, factors, Word_list)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Some description here')
    parser.add_argument('end_number', type=int, help="The length of the list you'd like to print, must be an integer value")
    parser.add_argument('--factors', nargs = "+", type = int, help = "A list of factor tuples, a printed number whose divisor is contained within this list will be substituted for the paired compound word in Word_list",)
    parser.add_argument('--Word_list', nargs = "+", type = str, help = "An optional list of compound words that will be paired with the factor list, must have the same length as the Factor List")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    print(args)
    print(type(args.Word_list))
    print(type(args.factors))
    main(args.end_number, args.factors, args.Word_list)
# main(end_number=101, factors=[3, 5, 7, 11, 4, 13, 6, 9], Word_list=['FizzBuzz', 'FangBang', 'SlamDunk', 'BingBang'])


