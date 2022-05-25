import pandas as pd
import numpy as np
import sys
from collections import Counter

allowed = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
all_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "#", "%" ]

"""Recognize combinations"""
all_lines = []
for line in sys.stdin:
    line_combs = []
    for i, char in enumerate(line[:-1]):
        char = char.lower()

        # Check first letter
        if char in allowed:
            s1 = char
        else:
            if char == ' ':
                s1 = '#'
            else:
                s1 = '%'

        # Check second letter
        char2 = line[i+1].lower()
        if char2 in allowed:
            s2 = char2
        else:
            if char2 == ' ':
                s2 = '#'
            else:
                s2 = '%'
        line_combs.append(f"{s1}-{s2}\t1")
    all_lines.append(line_combs.copy())

en_lines = 0
nl_lines = 0

for l in all_lines:
    df_guess = pd.DataFrame(np.zeros((28, 28)), columns=all_letters, index=all_letters)
    occ = dict(Counter(l))

    for k, v in occ.items():
        l1 = k[0]
        l2 = k[2]
        df_guess.at[l1, l2] = v

    total_count = df_guess.to_numpy().sum()
    for col in df_guess:
        df_guess[col] = df_guess[col].apply(lambda x: x/total_count)



    df_nl = pd.read_csv("NL.csv", index_col=0)
    df_en = pd.read_csv("EN.csv", index_col=0)

    # Calculate the differences between pre-trained matrices and input
    nl_diff_score = 0
    en_diff_score = 0

    df_nl_diff = pd.DataFrame(np.zeros((28, 28)), columns=all_letters, index=all_letters)
    df_en_diff = pd.DataFrame(np.zeros((28, 28)), columns=all_letters, index=all_letters)

    # Calculate differences between pre-trained matrices and input matrix.
    for col in range(len(df_nl)):
        for i in range(len(df_nl.iloc[0])):
            nl_diff_score += (float(df_guess.iat[i, col]) - float(df_nl.iat[i, col]))

    for col in range(len(df_en)):
        for i in range(len(df_en.iloc[0])):
            en_diff_score += (float(df_guess.iat[i, col]) - float(df_en.iat[i, col]))

    nl_diff_score = abs(nl_diff_score)
    en_diff_score = abs(en_diff_score)

    if nl_diff_score < en_diff_score:
        en_lines += 1

    elif en_diff_score < nl_diff_score:
        nl_lines += 1

    else:
        en_lines += 1

print(f"{en_lines} English lines\n"
      f"{nl_lines} Dutch lines")

# Print formatted results
expected_result = (73, 119)
accuracy = 100 - (abs(nl_lines - en_lines) / sum(expected_result) * 100)
print(f'Result: \nDutch sentences: {nl_lines} \nEnglish sentences: {en_lines}\n')
print(f'Expected result = Dutch sentences: {expected_result[0]}, English sentences: {expected_result[1]}')
print('Accuracy: ' + str(accuracy) + '%')
