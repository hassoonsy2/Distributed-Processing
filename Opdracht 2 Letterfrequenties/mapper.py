import sys


# All characters where our matrix consists of
SPACE = '_'
SPECIAL_CHARACTER = '!'
CHARACTER_SPLITTER = '-'

allowed = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]



if __name__ == "__main__":
    # Loop through all lines in file and create a matrix for each line
    for line in sys.stdin:
        line = line.strip()
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
            char2 = line[i + 1].lower()
            if char2 in allowed:
                s2 = char2
            else:
                if char2 == ' ':
                    s2 = '#'
                else:
                    s2 = '%'

            print('%s-%s\t%s' % (s1, s2, 1))
