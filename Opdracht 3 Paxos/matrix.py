import pandas as pd
import numpy as np


class Matrix:
    def __init__(self):
        all_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                       "t", "u", "v", "w", "x", "y", "z", "#", " "]

        self.df = pd.DataFrame(np.zeros((28, 28)), columns=all_letters, index=all_letters)

    def plus_one(self, column, row):
        """
        Adds one to a specific cell that is given.
        :param column: Given column
        :param row: Given row
        :return: None
        """
        self.df.at[column, row] += 1
