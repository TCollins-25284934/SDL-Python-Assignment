def generate_list():
    for i in range(1, 101):
        print(check_number(i))


def check_number(number):
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return number
def main():
    generate_list()
    
main()