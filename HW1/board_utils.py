# import numpy as np


class BoardUtils:
    def __init__(self):
        self.data = []

    def drawBoard(self, b):
        print('  0 1 2')
        for i in range(3):
            symbs = []
            # for x in b[i, :]:
            for x in b[i]:
                # print(x)
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

    def getStateFeatures(self, b, expressivity='full'):
        # x1 = np.count_nonzero(b == 1)
        # x2 = np.count_nonzero(b == -1)

        x1 = self.count2d(b, 1)
        x2 = self.count2d(b, -1)
        # x3 = self.count2d(b, 0)

        # features = [x1, x2]
        empty_xs_in_rows, empty_os_in_rows, empty_xs_in_cols, empty_os_in_cols, empty_xs_in_diags, empty_os_in_diags = self.getMinMovesToVictory(
            b)  # For opponent
        # print(self.getMinMovesToVictory(b))
        min_to_x_victory = empty_xs_in_rows + empty_xs_in_cols + empty_xs_in_diags
        min_to_o_victory = empty_os_in_rows + empty_os_in_cols + empty_os_in_diags
        if expressivity == 'compact':
            # min_to_x_victory = np.amin(min_to_x_victory)
            min_to_x_victory = min(min_to_x_victory)
            # min_to_o_victory = np.amin(min_to_o_victory)
            min_to_o_victory = min(min_to_o_victory)

            # min_to_o_victory = max(min_to_o_victory)
        # print(min_to_x_vic)
        # Seems to prefer winning wi 50% ai apponenent
        # return x1, x2, (min_to_x_victory), (min_to_o_victory)
        # Seems to prefer tying with 50% ai apponenent
        return x1, x2, (min_to_x_victory), (4-min_to_o_victory)

        # return features

    def evaluateBoardState(self, b, w, expressivity='full'):
        # self.getStateFeatures(b, expressivity)
        x1, x2, min_x_to_v, min_o_to_v = self.getStateFeatures(b, expressivity)
        # print(f'x1: {x1}')
        # print(f'x2: {x2}')
        # print(f'min_x_to_v: {min_x_to_v}')
        # print(f'min_o_to_v: {min_o_to_v}')
        if expressivity == 'compact':
            v_hat = w[0] + w[1]*x1 + w[2]*x2 + \
                w[3]*min_x_to_v + w[4]*min_o_to_v
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

    # def index_2d(self, b, val):
    #     rows = []
    #     cols = []
    #     for i, x in enumerate(b):
    #         for j, n in enumerate(x):
    #             if n == val:
    #                 rows.append(i)
    #                 cols.append(j)
    #                 # indices.append([i, j])
    #     return rows, cols

    def index_2d(self, b, val):
        # rows = []
        # cols = []
        indices = []
        for i, x in enumerate(b):
            for j, n in enumerate(x):
                if n == val:
                    # rows.append(i)
                    # cols.append(j)
                    indices.append([i, j])
        return indices

    def getMinMovesToVictory(self, b):
        empty_xs_in_rows = []
        empty_os_in_rows = []
        for r in range(3):
            # n_empty = np.count_nonzero(b[r, :] == 0)
            n_empty = self.count1d(b[r], 0)

            if n_empty < 3:
                # n_xs = np.count_nonzero(b[r, :] == 1)
                n_xs = self.count1d(b[r], 1)
                # n_os = np.count_nonzero(b[r, :] == -1)
                n_os = self.count1d(b[r], -1)

                # No one can win using this row (tie)
                if n_xs > 0 and n_os > 0:
                    empty_os_in_rows.append(4)
                    empty_xs_in_rows.append(4)
                    # empty_os_in_rows.append(3)
                    # empty_xs_in_rows.append(3)
                elif n_os == 0:  # No opponent marks in this row
                    # We can win using empty cells in row
                    empty_xs_in_rows.append(n_empty)
                    empty_os_in_rows.append(4)  # Opponent can't
                    # empty_os_in_rows.append(3)  # Opponent can't
                elif n_xs == 0:
                    empty_xs_in_rows.append(4)  # We can't win using this row
                    # Opponent can, using empty cells in row.
                    empty_os_in_rows.append(n_empty)
            else:  # Row is empty anyone can win using this row
                empty_xs_in_rows.append(n_empty)
                empty_os_in_rows.append(n_empty)

        # print(f'Min moves to win for X (rows): {empty_xs_in_rows}')
        # print(f'Min moves to win for O (rows): {empty_os_in_rows}')
        # print('----------------------------------------')

        empty_xs_in_cols = []
        empty_os_in_cols = []
        # How to address columns?
        b_T = self.transposeBoard(b)

        for c in range(3):
            # n_empty = np.count_nonzero(b[:, c] == 0)
            n_empty = self.count1d(b_T[c], 0)

            if n_empty < 3:
                # n_xs = np.count_nonzero(b[:, c] == 1)
                n_xs = self.count1d(b_T[c], 1)
                # n_os = np.count_nonzero(b[:, c] == -1)
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
        # print(f'Min moves to win for X (cols): {empty_xs_in_cols}')
        # print(f'Min moves to win for O (cols): {empty_os_in_cols}')
        # print('----------------------------------------')

        # diag1 = np.array([int(b[0][0]), int(b[1][1]), int(b[2][2])])
        # diag2 = np.array([int(b[0][2]), int(b[1][1]), int(b[2][0])])

        diag1 = [int(b[0][0]), int(b[1][1]), int(b[2][2])]
        diag2 = [int(b[0][2]), int(b[1][1]), int(b[2][0])]

        empty_xs_in_diags = []
        empty_os_in_diags = []
        # Check min moves to win along diagonals
        # n_empty = np.count_nonzero(diag1 == 0)
        n_empty = self.count1d(diag1, 0)
        # print(diag1)
        # print(f'Diag 1 empty: {n_empty}')
        # diag2_n_empty = np.count_nonzero(diag2 == 0)
        if n_empty < 3:
            # n_xs = np.count_nonzero(diag1 == 1)
            n_xs = self.count1d(diag1, 1)
            # n_os = np.count_nonzero(diag1 == -1)
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
        # print(f'Min moves to win for X (diag1): {empty_xs_in_diags}')
        # print(f'Min moves to win for O (diag1): {empty_os_in_diags}')
        # print('----------------------------------------')

        # n_empty = np.count_nonzero(diag2 == 0)
        n_empty = self.count1d(diag2, 0)
        # diag2_n_empty = np.count_nonzero(diag2 == 0)
        if n_empty < 3:
            # n_xs = np.count_nonzero(diag2 == 1)
            n_xs = self.count1d(diag2, 1)
            # n_os = np.count_nonzero(diag2 == -1)
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
        # print(f'Min moves to win for X (diags): {empty_xs_in_diags}')
        # print(f'Min moves to win for O (diags): {empty_os_in_diags}')
        # print('----------------------------------------')

        return empty_xs_in_rows, empty_os_in_rows, empty_xs_in_cols, empty_os_in_cols, empty_xs_in_diags, empty_os_in_diags

    def getLegalMoves(self, b):
        # Will return coordinates of cell to place 1 in
        # rows, cols = np.where(b == 0)
        return self.index_2d(b, 0)
        # legalMoves = []
        # for idx in indices:
        #     legalMoves.append([idx[0], idx[1]])
        # print(f'Indices: {indices}')
        # print(f'Legal moves: {legalMoves}')
        # return legalMoves

    def invertBoard(self, b):
        invertedBoard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        selfPos = self.index_2d(b, 1)
        oppnPos = self.index_2d(b, -1)

        # if len(selfPos) > 0:
        for pos in selfPos:
            # print(pos)
            invertedBoard[pos[0]][pos[1]] = -1
        for pos in oppnPos:
            invertedBoard[pos[0]][pos[1]] = 1

        return invertedBoard

    def isEmpty(self, b):
        return self.count2d(b, 0) == 9

    def gameWon(self, b, val):
        # Check for
        won = False
        # if (np.count_nonzero(b == val) < 3):
        if (self.count2d(b, val) < 3):
            won = False
            # Check about to win stituations
            # There is only one cell left
        else:
            b_T = self.transposeBoard(b)
            for i in range(3):
                # Check rows and cols for victory
                # if (np.count_nonzero(b[i, :] == val) == 3 or np.count_nonzero(b[:, i] == val) == 3):
                #     won = True
                if (self.count1d(b[i], val) == 3 or self.count1d(b_T[i], val) == 3):
                    won = True
            # diag1 = np.array([int(b[0][0]), int(b[1][1]), int(b[2][2])])
            # diag2 = np.array([int(b[0][2]), int(b[1][1]), int(b[2][0])])
            diag1 = [int(b[0][0]), int(b[1][1]), int(b[2][2])]
            diag2 = [int(b[0][2]), int(b[1][1]), int(b[2][0])]
            # Check diags for victory
            if (self.count1d(diag1, val) == 3 or self.count1d(diag2, val) == 3):
                won = True
        return won

    def gameTie(self, b):
        # return np.count_nonzero(b == 0) == 0 and not self.gameWon(b, 1) and not self.gameWon(b, -1)
        return self.count2d(b, 0) == 0 and not self.gameWon(b, 1) and not self.gameWon(b, -1)

    def isFinalState(self, b):
        return self.gameTie(b) or self.gameWon(b, 1) or self.gameWon(b, -1)
