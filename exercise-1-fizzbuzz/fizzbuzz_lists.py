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

    * split_string - Splits a string in half, in the case of uneven strings, the function will load the back half
    * split_string_list - Splits a list of strings in half using the split_string function
    * check_number - Determines the appropriate output for a number based on its factors and the corresponding compound words.
    * validate_inputs - Validates factor and compound word inputs.
    * main - the main function of the script
"""
import argparse

def generate_list(end_number, Factor_list, Compword_list):
    """
    Generates and prints a custom FizzBuzz sequence from 1 up to
    the specified end number and prints either the
    number itself or a replacement string determined by the factor pairs
    and compound words provided.

    Parameters
    ----------
    end_number : int
        The final number in the sequence.

    Factor_list : list[int]
        A list of factor pairs.
        Example: [3, 5, 7, 11].

    Compword_list : list[str]
        A list of compound words corresponding to the factor pairs.

    Returns
    -------
    None
        Prints the sequence to the console.
    """
    for i in range(1, end_number+1):
        print(check_number(i, Factor_list, Compword_list))

def split_string(given_str):
    """
    Split a string into two halves. If the string is uneven in length it will split the word with
    the extra character in the second half.

    Parameters
    ----------
    given_str : str
        The string to be split.

    Returns
    -------
    a, b : tuple[str, str]
        A tuple containing the first and second halves
        of the string.
    """
    a, b = given_str[:len(given_str)// 2], given_str[len(given_str)// 2:]
    return a, b

def split_string_list(CompWord_list):
    """
    Split each compound word in a list into two halves using the split_string function.

    Parameters
    ----------
    CompWord_list : list[str]
    A list of compound words.

    Returns
    -------
    starts, ends : tuple[list[str], list[str]]
    Two lists containing the first and second halves
    of each compound word.
    """
    starts = []
    ends = []
    for CompWord in CompWord_list:
        starts.append(split_string(CompWord)[0])
        ends.append(split_string(CompWord)[1])
    return starts, ends

def check_number(number, intuple_list, CompWord_list):
    """
    Determines the correct output for a number in the
    FizzBuzz sequence.

    A number divisible by the first factor in a pair receives
    the first half of the corresponding compound word. A number
    divisible by the second factor receives the second half.
    A number divisible by both factors receives the complete
    compound word.
    A number divisible by factors across two inputted factor pairs will receive
    a corresponding mix of compound words.
    A number divisible by 3 or more factors across the factor pairs will
    receive a frankenstein of corresponding compound word halves.

    Parameters
    ----------
    number : int
        The number to evaluate.

    intuple_list : list[int]
        A list of factor pairs.

    CompWord_list : list[str]
        A list of compound words corresponding to the factor pairs.

    Returns
    -------
    result : str or int
        The generated replacement string if a factor match exists,
        otherwise the original number.
    """

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

def validate_inputs(factors, word_list):
    """
    Validates user input before generating the sequence.

    Ensures that factors are supplied in pairs, that the number
    of compound words matches the number of factor pairs,
    that each compound word can be split evenly, and a factor is not 0.

    Parameters
    ----------
    factors : list[int]
        A list of factor pairs.

    word_list : list[str]
        A list of compound words.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        Raised when the inputs are invalid.
    """

    if len(factors) % 2 != 0:
        raise ValueError("Factors must be supplied in pairs.")

    if len(word_list) != len(factors) // 2:
        raise ValueError("The number of compound words must match the number of factor pairs.")

    for factor in factors:
        if factor == 0:
            raise ValueError("Factors cannot be zero.")

    for word in word_list:
        if len(word) % 2 != 0:
            raise ValueError(f"'{word}' cannot be split evenly. Compound words must have an even number of characters.")

def main(end_number, factors, Word_list):
    validate_inputs(factors, Word_list)

    generate_list(end_number, factors, Word_list)


def parse_arguments():
    parser = argparse.ArgumentParser(description="""Custom FizzBuzz generator.\n
                                                    Examples:\n
                                                    python fizzbuzz.py\n
                                                    python fizzbuzz.py --end_number 50\n
                                                    python fizzbuzz.py --factors 3 5 7 11 --Word_list FizzBuzz BingBong\n
                                                    \n
                                                    Note:\n
                                                    Factors are entered as space-separated values, not comma-separated.\n
                                                    The example above creates the factor pairs (3,5) and (7,11).""")
    parser.add_argument('--end_number', type=int, default= 100, help="The length of the list you'd like to print, must be an integer value")
    parser.add_argument('--factors', nargs = "+", type = int, default = [3,5], help = "A space separated list of factor pairs, a printed number whose divisor is contained within this list will be substituted for the corresponding compound word in Word_list",)
    parser.add_argument('--Word_list', nargs = "+", type = str, default = ["FizzBuzz"], help = "A space separated list of compound words that will be paired with the factor list, must have the same length as the factor List")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.end_number, args.factors, args.Word_list)


