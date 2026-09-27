def generate_list():
    for i in range(1, 101):
        print(check_number(i, "FizzBuzz", (3,5)))

def split_string(given_str):
    a, b = given_str[:len(given_str)// 2], given_str[len(given_str)// 2:]
    return a, b

def check_number(number, CompWord, intuple):
    start, end = split_string(CompWord)
    if number % intuple[0] == 0 and number % intuple[1] == 0:
        return CompWord
    elif number % intuple[0] == 0:
        return start
    elif number % intuple[1] == 0:
        return end
    else:
        return number

def main():
    generate_list()

main()