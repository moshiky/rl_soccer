#!/usr/bin/env python2

from Field import Field
from QLearner import QLearner
from OpponentStrategy import OpponentStrategy
from constans import *
from logger import Logger


def printSettings():
    if (USE_SIMILARITIES):
        print "Using similarities"
    else:
        print "Without similarities"

    if (USE_DECAY):
        print "Using decay"
    else:
        print "Without decay"

    print "alpha:", ALPHA

def main():
    # for x in xrange(1,100000):

    printSettings()

    qRun()

    printSettings()


def qRun():
    logger = Logger()
    field = Field(logger)
    Q = QLearner('b', ownStatesOnly = True)
    opponentStrategy = OpponentStrategy('a')
    
    repetition = 10000

    trainBatchSize = 50
    testBatchSize = 10000
    gamesToPlayInitial = 1000

    train_stats = list()

    field.test(Q, opponentStrategy, testBatchSize)

    b_wins_counter = [0]*int(gamesToPlayInitial / trainBatchSize)

    for i in range(repetition):
        train_stats.append([0]*int(gamesToPlayInitial / trainBatchSize))
        logger.log("--- rep {0} ---".format(i))
        gamesToPlay = gamesToPlayInitial

        Q = QLearner('b', ownStatesOnly = True)

        currentIndex = 0

        while gamesToPlay > 0:

            logger.log('-- train')
            train_stats[i][currentIndex] += \
                field.train(Q, opponentStrategy, trainBatchSize, trainMode=True, printStat=True, printGame=False)

            logger.log('-- test')
            b_wins_counter[currentIndex] += field.test(Q, opponentStrategy, testBatchSize)

            gamesToPlay -= trainBatchSize
            currentIndex += 1

    train_stats = map(lambda r: r/float(repetition), train_stats)
    b_wins_counter = map(lambda r: r/float(repetition), b_wins_counter)

    logger.log('train mean: ' + ','.join(map(str, train_stats)))
    logger.log('eval mean: ' + ','.join(map(str, b_wins_counter)))

    # print Q

    # import pickle
    # with open('q_table3', 'wb') as f:
    #     pickle.dump( Q, f)

if __name__ == '__main__':
    main()
