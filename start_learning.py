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
    
    repetition = 4

    trainBatchSize = 50
    testBatchSize = 1000
    gamesToPlayInitial = 1000


    field.test(Q, opponentStrategy, testBatchSize)

    a_wins_counter = [0]*int(gamesToPlayInitial / trainBatchSize)


    for i in xrange(1,repetition):

        logger.log("-----------")
        gamesToPlay = gamesToPlayInitial

        Q = QLearner('b', ownStatesOnly = True)

        currentIndex = 0

        while (gamesToPlay > 0):

            field.train(Q, opponentStrategy, trainBatchSize, trainMode = True, printStat = False, printGame = False)

            a_wins_counter[currentIndex] += field.test(Q, opponentStrategy, testBatchSize)

            gamesToPlay -= trainBatchSize

            currentIndex += 1

    a_wins_counter = [i/(repetition-1) for i in a_wins_counter]
    log_msg = "\n"
    for x in a_wins_counter:
        log_msg += '{x_val}\n'.format(x_val=x)
    logger.log(log_msg)

    print Q

    import pickle
    with open('q_table3', 'wb') as f:
        pickle.dump( Q, f)

if __name__ == '__main__':
    main()
