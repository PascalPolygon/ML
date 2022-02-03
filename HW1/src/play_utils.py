import os
from board_utils import BoardUtils
from critic import Critic
from generalizer import Generalizer
from perf_system import PerfSystem

board_utils = BoardUtils()
critic = Critic()
generalizer = Generalizer()
perf_system = PerfSystem()


class PlayUtils:
    def __init__(self, dojoFilePath):
        self.data = []
        self.DOJO_FILE_PATH = dojoFilePath

    def test(self, weights, expressivity):
        gameOn = True
        print(self.DOJO_FILE_PATH)
        nWins = 0
        nLosses = 0
        nTies = 0
        nGames = 0
        # Check if file is empty
        if os.path.getsize(self.DOJO_FILE_PATH) == 0:
            print('File is empty')
            dojoFile = open(self.DOJO_FILE_PATH, "w")  # Open in writing mode
        else:
            print('File is not empty')
            dojoFile = open(self.DOJO_FILE_PATH, "a")  # Open in append mode
        print('Testing')
        while gameOn:
            a = ''
            a = input("Hello human, do you want to go first? (y/n), q to quit: ")
            b = [[0, 0, 0],  # init board
                 [0, 0, 0],
                 [0, 0, 0]]
            if a == 'y' or a == 'Y':
                print('Ok, you go first!')
                board_utils.drawBoard(b)
                # Input rows and cols to play and drawboard
                gameOn = True
                while(not board_utils.isFinalState(b)):
                    nb = self.playerMove(b)
                    while not nb:
                        nb = self.playerMove(b)
                    b = nb
                    if self.gameOver(b):
                        break
                    # COmputer move
                    b = self.computerMove(b, weights, expressivity)
                    self.addToTrainingFile(dojoFile, b)
                    print('------------------------------------------')
                # Update performance stats
                nGames += 1
                if board_utils.gameWon(b, 1):
                    nWins += 1
                elif board_utils.gameWon(b, -1):
                    nLosses += 1
                elif board_utils.gameTie(b):
                    nTies += 1
                self.gameOver(b)
                self.addToTrainingFile(dojoFile, b, critic.getFinalScore(b))
            elif a == 'n' or a == 'N':
                print('Ok, I go first!')
                # perf_sytem makes first move and drawboard
                gameOn = True
                while(not board_utils.isFinalState(b)):
                    if board_utils.isEmpty(b):
                        # Random move to start the game
                        b = perf_system.chooseRandomMove(b)
                        self.addToTrainingFile(dojoFile, b)
                        board_utils.drawBoard(b)
                    else:
                        b = self.computerMove(b, weights, expressivity)

                    if self.gameOver(b):
                        break
                    nb = self.playerMove(b)
                    while not nb:
                        nb = self.playerMove(b)
                    b = nb
                    self.addToTrainingFile(dojoFile, b)
                    print('------------------------------------------')
                # Update performance stats
                nGames += 1
                if board_utils.gameWon(b, 1):
                    nWins += 1
                elif board_utils.gameWon(b, -1):
                    nLosses += 1
                elif board_utils.gameTie(b):
                    nTies += 1
                self.gameOver(b)
                self.addToTrainingFile(dojoFile, b, critic.getFinalScore(b))
            elif a == 'q' or a == 'Q':
                print('Bye-bye!')
                gameOn = False
                dojoFile.close()

        if nGames > 0:
            return nGames, [nWins/nGames, nLosses/nGames, nTies/nGames]
        else:
            return nGames, [0, 0, 0]

    def addToTrainingFile(self, dojoFile, b, finalScore=None):
        for r in b:
            dojoFile.write(f'{r}; ')
        if finalScore is not None:
            dojoFile.write(f'{finalScore}')
        dojoFile.write('\n')

    def gameOver(self, b):
        if (board_utils.isFinalState(b)):
            if (board_utils.gameWon(b, 1)):
                print('Computer win!')
            elif (board_utils.gameWon(b, -1)):
                print('You win')
            return True
        else:
            return False

    def getPlayerMove(self):
        print('Enter your move, use row (0-2) and column (0-2) numbers')
        r = input("row number: ")
        c = input('col number: ')
        try:
            r = int(r)
            c = int(c)
        except ValueError:
            print('**[ERROR] Input must an integer')
            return None

        if r < 0 or r > 2 or c < 0 or c > 2:
            print('**[ERROR] You can only use numbers: (0,1,2)')
            return None
            # continue
        print(f'Your move = [{r} {c}]')
        return r, c

    def playerMove(self, b):
        move = self.getPlayerMove()
        if move is None:
            return False
        else:
            r, c = move
            b[r][c] = -1
            board_utils.drawBoard(b)
            return b

    def computerMove(self, b, weights, expressivity):
        print('Computer move:')
        b = perf_system.play(b, weights, expressivity)
        board_utils.drawBoard(b)
        return b
