import numpy as np


class BoardUtils:
    def __init__(self):
        self.data = []

    def drawBoard(self, b):
        print('  0 1 2')
        for i in range(3):
            symbs = []
            for x in b[i, :]:
                # print(x)
                if x == 0:
                    symbs.append(' ')
                elif x == -1:
                    symbs.append('O')
                else:
                    symbs.append('X')
            print(f'{i} '+symbs[0]+"|"+symbs[1]+"|"+symbs[2])
            print('  '+'-'+'+'+'-'+'+'+'-')

    def getStateFeatures(self, b):
        x1 = np.count_nonzero(b == 1)
        x2 = np.count_nonzero(b == -1)
        features = [x1, x2]
        print(features)
        self.getMinMovesToVictory(b, -1)  # For opponent
        return features

    def getMinMovesToVictory(self, b, val):
        pos = np.where(b == val)
        print(pos)
        # Check rows
        print(len(pos))
        print(pos[0].shape)
        rows = pos[0]
        cols = pos[1]
        print(rows)
        print(cols)
        for r in rows:
            # see how many are empy in row r
            row_empty = np.count_nonzero(b[r, :] == 0)
            # note: row_empty == 0 is a state where teh row is full but there is no winner. Because if it's 9 and we get to to play again, it is not full due to the same mark in a row. FOr this reason, we can assign this a value of 4 or is 3 better?
            print(f'empty in row {r} : {row_empty}')
        for c in cols:
            col_empty = np.count_nonzero(b[:, c] == 0)
            print(f'empty in col {c} : {col_empty}')
            # See how many are empty in col c
        # See how many are empty along diag

        # for r in rows:
        #     row = p[0]
        # check row
