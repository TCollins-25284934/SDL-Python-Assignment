import random

def powertracker():
    i =0
    nums = []
    flag = False
    while flag == False:
        choose = bool(random.randint(0,1))
        num = random.randint(1,20)
        if choose:
            new_num = num **3
            nums.append(new_num)
            print(f"Loop {i}: {num}^3 = {new_num}")
        else:
            new_num = num**2
            nums.append(new_num)
            print(f"Loop {i}: {num}^2 = {new_num}")
        print(new_num, nums[i-1])
        if new_num % nums[i-1] == 0 and i != 0:
            flag = True
        i += 1

    print(f"the maximum number recorded was {max(nums)}")
    print(f"the minimum number recorded was {min(nums)}")

def main():
    powertracker()
main()