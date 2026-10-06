"""Powertracker

This script will repeatedly generate a random integer between 1 and 20 and:
1. Randomly choose whether to square or cube this number;
2. Store the squared or cubed result;
3. Track the largest and smallest results;
4. Check if the current result is divisible by the previous result, if so the programme will end;
5. Print to the console  the largest and smallest of the squared or cubed numbers,
which two numbers caused the loop to break, and the total number of iterations that the program completed

The number 1 is excluded from comparison, as everything is divisible by 1

"""

import random
import argparse

def powertracker():
    """
    Generates random squared and cubed numbers until one is divisible by the previous number.

    During each iteration, a random integer between 1 and 20 is
    generated and either squared or cubed. The result is stored and
    compared against the previous result. 

    The function tracks and reports:
        * The result generated during each iteration.
        * The pair of results that caused the loop to terminate.
        * The total number of iterations completed.
        * The largest result generated.
        * The smallest result generated.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Prints the generated results and summary statistics
        to the console.
    """
    i =0
    nums = []
    flag = False
    while flag == False:
        choose = bool(random.randint(0,1))
        num = random.randint(1,20)
        if choose:
            new_num = num **3
            nums.append(new_num)
            print(f"Loop {i+1}: {num}^3 = {new_num}")
        else:
            new_num = num**2
            nums.append(new_num)
            print(f"Loop {i+1}: {num}^2 = {new_num}")
        # print(new_num, nums[i-1])
        if new_num % nums[i-1] == 0 and i != 0 and nums[i-1] != 1:
            print(f"{new_num} is divisible by {nums[i-1]}")
            flag = True
            print(f"We completed {i+1} loops")
        i += 1

    print(f"the maximum number recorded was {max(nums)}")
    print(f"the minimum number recorded was {min(nums)}")

def main():
    powertracker()
# main()
def parse_arguments():
    parser = argparse.ArgumentParser(description="""PowerTracker
                                                    
                                                    Repeatedly generates random integers between 1 and 20 and
                                                    randomly squares or cubes them.
                                                    
                                                    The programme tracks:
                                                    * The largest generated value.
                                                    * The smallest generated value.
                                                    * The number of iterations completed.
                                                    
                                                    The programme terminates when the current generated value
                                                    is divisible by the previous generated value.
                                                    
                                                    Example:
                                                    python powertracker.py""")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    main()