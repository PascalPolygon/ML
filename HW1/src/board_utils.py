# import numpy as np


class BoardUtils:
    def __init__(self):
        self.data = []

    def drawBoard(self, b):
        print('  0 1 2')
        for i in range(3):
            symbs = []
            for x in b[i]:
                if x == 0:
                    symbs.append(' ')
                elif x == -1:
                    symbs.append('O')
                else:
                    symbs.append('X')
            print(f'{i} '+symbs[0]+"|"+symbs[1]+"|"+symbs[2])
            print('  '+'-'+'+'+'-'+'+'+'-')

    def count2d(self, b, val):
        return sum(x == val for row in b for x in row)

    def count1d(self, r, val):
        return sum(x == val for x in r)

    def getStateFeatures(self, b, expressivity):
        x1 = self.count2d(b, 1)
        x2 = self.count2d(b, -1)

        empty_xs_in_rows, empty_os_in_rows, empty_xs_in_cols, empty_os_in_cols, empty_xs_in_diags, empty_os_in_diags = self.getMinMovesToVictory(
            b, expressivity)  # For opponent

        min_to_x_victory = empty_xs_in_rows + empty_xs_in_cols + empty_xs_in_diags
        min_to_o_victory = empty_os_in_rows + empty_os_in_cols + empty_os_in_diags
        if expressivity == 'compact':
            min_to_x_victory = min(min_to_x_victory)
            min_to_o_victory = min(min_to_o_victory)

        # Seems to prefer winning wi 50% ai apponenent
        return x1, x2, min_to_x_victory, min_to_o_victory
        # Seems to prefer tying with 50% ai apponenent
        # return x1, x2, (min_to_x_victory), (4-min_to_o_victory)

    def evaluateBoardState(self, b, w, expressivity):
        x1, x2, min_x_to_v, min_o_to_v = self.getStateFeatures(b, expressivity)
        if expressivity == 'compact':
            v_hat = w[0] + w[1]*x1 + w[2]*x2 + \
                w[3]*min_x_to_v + w[4]*min_o_to_v
            return v_hat
        elif expressivity == 'full':
            x3 = min_x_to_v[0]
            x4 = min_x_to_v[1]
            x5 = min_x_to_v[2]
            # cols
            x6 = min_x_to_v[3]
            x7 = min_x_to_v[4]
            x8 = min_x_to_v[5]

            # diags
            x9 = min_x_to_v[6]
            x10 = min_x_to_v[7]
            # opponent
            # rows
            x11 = min_o_to_v[0]
            x12 = min_o_to_v[1]
            x13 = min_o_to_v[2]
            # cols
            x14 = min_o_to_v[3]
            x15 = min_o_to_v[4]
            x16 = min_o_to_v[5]
            # diags
            x17 = min_o_to_v[6]
            x18 = min_o_to_v[7]

            v_hat = w[0] + w[1]*x1 + w[2]*x2 + \
                w[3]*x3 + w[4]*x4 + w[5]*x5 + w[6] * \
                x6 + w[7]*x7 + w[8]*x8 + w[9]*x9 + \
                w[10]*x10 + w[11]*11 + w[12]*12 + \
                w[13]*13 + w[14]*x14 + w[15]*x15 + \
                w[16]*x16 + w[17]*x17 + w[18]*x18
            return v_hat

    def transposeBoard(self, b):
        b_T = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        b_T[0][0] = b[0][0]  # same
        b_T[0][1] = b[1][0]
        b_T[0][2] = b[2][0]

        b_T[1][0] = b[0][1]
        b_T[1][1] = b[1][1]  # same
        b_T[1][2] = b[2][1]

        b_T[2][0] = b[0][2]
        b_T[2][1] = b[1][2]
        b_T[2][2] = b[2][2]  # same
        return b_T

    def index_2d(self, b, val):
        indices = []
        for i, x in enumerate(b):
            for j, n in enumerate(x):
                if n == val:
                    indices.append([i, j])
        return indices

    def getMinMovesToVictory(self, b, expressivity):
        empty_xs_in_rows = []
        empty_os_in_rows = []
        for r in range(3):
            n_empty = self.count1d(b[r], 0)

            if n_empty < 3:
                n_xs = self.count1d(b[r], 1)
                n_os = self.count1d(b[r], -1)

                # No one can win using this row (tie)
                if n_xs > 0 and n_os > 0:
                    empty_os_in_rows.append(4)
                    empty_xs_in_rows.append(4)
                elif n_os == 0:  # No opponent marks in this row
                    # We can win using empty cells in row
                    empty_xs_in_rows.append(n_empty)
                    empty_os_in_rows.append(4)  # Opponent can't
                elif n_xs == 0:
                    empty_xs_in_rows.append(4)  # We can't win using this row
                    # Opponent can, using empty cells in row.
                    empty_os_in_rows.append(n_empty)
            else:  # Row is empty anyone can win using this row
                empty_xs_in_rows.append(n_empty)
                empty_os_in_rows.append(n_empty)

        empty_xs_in_cols = []
        empty_os_in_cols = []

        b_T = self.transposeBoard(b)

        for c in range(3):
            n_empty = self.count1d(b_T[c], 0)

            if n_empty < 3:
                n_xs = self.count1d(b_T[c], 1)
                n_os = self.count1d(b_T[c], -1)

                # No one can win using this row (tie)
                if n_xs > 0 and n_os > 0:
                    empty_os_in_cols.append(4)
                    empty_xs_in_cols.append(4)
                elif n_os == 0:  # No opponent marks in this row
                    # We can win using empty cells in row
                    empty_xs_in_cols.append(n_empty)
                    empty_os_in_cols.append(4)  # Opponent can't
                elif n_xs == 0:
                    empty_xs_in_cols.append(4)  # We can't win using this row
                    # Opponent can, using empty cells in row.
                    empty_os_in_cols.append(n_empty)
            else:  # Row is empty anyone can win using this row
                empty_xs_in_cols.append(n_empty)
                empty_os_in_cols.append(n_empty)

        diag1 = [int(b[0][0]), int(b[1][1]), int(b[2][2])]
        diag2 = [int(b[0][2]), int(b[1][1]), int(b[2][0])]

        empty_xs_in_diags = []
        empty_os_in_diags = []
        # Check min moves to win along diagonals
        n_empty = self.count1d(diag1, 0)
        if n_empty < 3:
            n_xs = self.count1d(diag1, 1)
            n_os = self.count1d(diag1, -1)

            # No one can win using this row (tie)
            if n_xs > 0 and n_os > 0:
                empty_os_in_diags.append(4)
                empty_xs_in_diags.append(4)
            elif n_os == 0:  # No opponent marks in this row
                # We can win using empty cells in row
                empty_xs_in_diags.append(n_empty)
                empty_os_in_diags.append(4)  # Opponent can't
            elif n_xs == 0:
                empty_xs_in_diags.append(4)  # We can't win using this row
                # Opponent can, using empty cells in row.
                empty_os_in_diags.append(n_empty)
        else:  # Row is empty anyone can win using this row
            empty_xs_in_diags.append(n_empty)
            empty_os_in_diags.append(n_empty)

        n_empty = self.count1d(diag2, 0)
        if n_empty < 3:
            n_xs = self.count1d(diag2, 1)
            n_os = self.count1d(diag2, -1)

            # No one can win using this row (tie)
            if n_xs > 0 and n_os > 0:
                empty_os_in_diags.append(4)
                empty_xs_in_diags.append(4)
            elif n_os == 0:  # No opponent marks in this row
                # We can win using empty cells in row
                empty_xs_in_diags.append(n_empty)
                empty_os_in_diags.append(4)  # Opponent can't
            elif n_xs == 0:
                empty_xs_in_diags.append(4)  # We can't win using this row
                # Opponent can, using empty cells in row.
                empty_os_in_diags.append(n_empty)
        else:  # Row is empty anyone can win using this row
            empty_xs_in_diags.append(n_empty)
            empty_os_in_diags.append(n_empty)

        if expressivity == 'full':
            for i in range(len(empty_xs_in_rows)):
                empty_xs_in_rows[i] = empty_xs_in_rows[i]
            for i in range(len(empty_os_in_rows)):
                empty_os_in_rows[i] = empty_os_in_rows[i]
            for i in range(len(empty_xs_in_cols)):
                empty_xs_in_cols[i] = empty_xs_in_cols[i]
            for i in range(len(empty_os_in_cols)):
                empty_os_in_cols[i] = empty_os_in_cols[i]
            for i in range(len(empty_xs_in_diags)):
                empty_xs_in_diags[i] = empty_xs_in_diags[i]
            for i in range(len(empty_os_in_diags)):
                empty_os_in_diags[i] = empty_os_in_diags[i]

        # for i in range(len(empty_xs_in_rows)):
        #     empty_xs_in_rows[i] = empty_xs_in_rows[i]
        # for i in range(len(empty_os_in_rows)):
        #     empty_os_in_rows[i] = empty_os_in_rows[i]
        # for i in range(len(empty_xs_in_cols)):
        #     empty_xs_in_cols[i] = empty_xs_in_cols[i]
        # for i in range(len(empty_os_in_cols)):
        #     empty_os_in_cols[i] = empty_os_in_cols[i]
        # for i in range(len(empty_xs_in_diags)):
        #     empty_xs_in_diags[i] = empty_xs_in_diags[i]
        # for i in range(len(empty_os_in_diags)):
        #     empty_os_in_diags[i] = empty_os_in_diags[i]

        # return (4-empty_xs_in_rows), (4-empty_os_in_rows), (4-empty_xs_in_cols), (4 - empty_os_in_cols), (4-empty_xs_in_diags), (4-empty_os_in_diags)
        return empty_xs_in_rows, empty_os_in_rows, empty_xs_in_cols, empty_os_in_cols, empty_xs_in_diags, empty_os_in_diags

    def getLegalMoves(self, b):
        return self.index_2d(b, 0)

    def invertBoard(self, b):
        invertedBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        selfPos = self.index_2d(b, 1)
        oppnPos = self.index_2d(b, -1)

        for pos in selfPos:
            invertedBoard[pos[0]][pos[1]] = -1
        for pos in oppnPos:
            invertedBoard[pos[0]][pos[1]] = 1

        return invertedBoard

    def isEmpty(self, b):
        return self.count2d(b, 0) == 9

    def gameWon(self, b, val):
        won = False
        if (self.count2d(b, val) < 3):
            won = False
        else:
            b_T = self.transposeBoard(b)
            for i in range(3):
                # Check rows and cols for victory
                if (self.count1d(b[i], val) == 3 or self.count1d(b_T[i], val) == 3):
                    won = True
            diag1 = [int(b[0][0]), int(b[1][1]), int(b[2][2])]
            diag2 = [int(b[0][2]), int(b[1][1]), int(b[2][0])]
            # Check diags for victory
            if (self.count1d(diag1, val) == 3 or self.count1d(diag2, val) == 3):
                won = True
        return won

    def gameTie(self, b):
        return self.count2d(b, 0) == 0 and not self.gameWon(b, 1) and not self.gameWon(b, -1)

    def isFinalState(self, b):
        return self.gameTie(b) or self.gameWon(b, 1) or self.gameWon(b, -1)
