# Letter frequency
#Student : Hussin Almoustafa 

### Setup:
1. Clone this repository
2. Make sure you have `pandas` and `numpy` installed with `pip install pandas` and `pip install numpy`

## How to run:
### Train:
1. I made sure I had good English and Dutch train examples in `input_en.txt` and `input_nl.txt`.
2. I used the `matrix_create.py` file to create a .csv-file that contains a matrix for a language.
3. Change the output file name to `"EN.csv"` or `"NL.csv"`, depending on which language you're trying to train on.
4. Run `type input_en.txt | python mapper.py | sort | python reducer.py | python matrix_create.py` to generate a .csv-file
5. Do this for both Dutch and English.

### Test:
1. Insert your input text in `input.txt`.
2. Run the testwith `type test_file.txt | python language_guesser.py`


### Result:

```
Dutch sentences: 107
English sentences: 85

Expected result = Dutch sentences: 73, English sentences: 119
Accuracy: 88.54166666666667%

```
> Your code works properly if 73 Dutch and 119 English lines are recognized. 

