# Exercise-1-fizzbuzz
fizzbuzz.py is a script that runs the "fizzbuzz" mathematical game. With no arguments passed in the game will default to playing with a list length
of 100 digits, a factor pair of 3 and 5, and the compound word "FizzBuzz". Users may pass in three arguments to adapt the game: the length of the
number list they'd like to play with, as many pairs of factors as they'd like, and a corresponding number of compound words that will be printed when
the correct factor is identified.
A number divisible by the first factor in a pair receives the first half of the corresponding compound word.
A number divisible by the second factor receives the second half.
A number divisible by both factors receives the complete compound word.

A number divisible by factors across two inputted factor pairs will receive a corresponding mix of compound words.
A number divisible by 3 or more factors across the factor pairs will receive a frankenstein of corresponding compound word halves.

Examples
---------------
python fizzbuzz.py

python fizzbuzz.py --end_number 50

python fizzbuzz.py --end_number 50 --factors 3 5 7 11 --Word_list FizzBuzz BingBong


## Exercise-2-powertracker
powertracker.py is a script that repeatedly generate a random integer between 1 and 20 and:
1. Randomly choose whether to square or cube this number;
2. Store the squared or cubed result;
3. Track the largest and smallest results;
4. Check if the current result is divisible by the previous result, if so the programme will end;
5. Print to the console  the largest and smallest of the squared or cubed numbers,
which two numbers caused the loop to break, and the total number of iterations that the program completed

The number 1 is excluded from comparison, as everything is divisible by 1

No arguments are needed.

Examples
---------------
python powertracker.py


## Exercise-3-spectrum
The spectrum.py script will parse spectrum emission data from a .txt file and plot the flux versus wavelength. 
The script will then fit:
1. A third order polynomial continuum to the plot, excluding a 10 unit window around the peak flux
2. A gaussian function to the plot within a 10 unit window of the peak flux
3. The combined gaussian and continuum model over the whole dataset.
The script will output to the console the best fit parameters of the combined model.

The script takes one argument in the filepath of the file.
The script will accept any valid file path provided on the command line and can open files located anywhere on the system, provided the file exists, is readable, and matches the expected spectrum data format. 
If the file is in the same directory (such as the spectrum.txt file provided here) then it is sufficient to pass the filename alone, see the second example below

Examples
---------------
python spectrum.py ...\spectrum.txt

python spectrum.py spectrum.txt



## Exercise-4-apollo
The parser.py script will parse flight data from a file with a specific format.
The input file must follow the expected flight-data format i.e. comments and return characters have a leading "$" character (and are ignored during parsing), a comma separated table data with no leading characters, and the first two rows of the table contain header information and units respectively.

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
