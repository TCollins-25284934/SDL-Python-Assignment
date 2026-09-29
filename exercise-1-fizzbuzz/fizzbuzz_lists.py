def generate_list(end_number):
    for i in range(1, end_number+1):
        check_number(i, ["FizzBuzz","FangBang", 'SlamDunk'], [(3,5),(7,11),(4,13)])

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
    print(starts)
    print(ends)
    for i,j in enumerate(dct.keys()):
        print(i,j)
        print(starts[i])
        print(ends[i])
        print(dct[j])
    for i,j in enumerate(dct.keys()):
        # print(number)
        # print(i,j, dct[j])
        # print(starts[i], ends[i], CompWord_list[i])
        pass
    #     if number % j == 0 and number % dct[j]== 0:
    #         return CompWord_list[i]
    #
    #     elif number % j == 0:
    #         return starts[i]
    #
    #     elif number % dct[j] == 0:
    #         return ends[i]
    #
    # else:
    #     return number
def main():
    generate_list(102)

main()