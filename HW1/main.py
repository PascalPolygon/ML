# import sys
# import logging
from experiment_generator import ExperimentGenerator
from board_utils import BoardUtils
from perf_system import PerfSystem

# logging.basicConfig(level=logging.INFO)
# logging.info('Hello world!')
# logging.basicConfig(level=logging.NOTSET)
# logger = logging.getLogger('main')


def main():
    exp_gen = ExperimentGenerator(0.8)
    board_utils = BoardUtils()
    perf_system = PerfSystem()

    weights = [0.1, 0.1, 0.1, 0.1, 0.1]
    b = exp_gen.generateBoard(weights)
    print(b)
    if b is not None:
        b[1][1] = -1
        print(b)
        board_utils.drawBoard(b)
        perf_system.play(b, weights)

    # print(b)
    # logger.info(b)


if __name__ == '__main__':
    # logger.info('Hello world!')
    # print('Hello world!')

    main()
    # sys.exit(main())
