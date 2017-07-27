import copy
import random
from constans import *

from similarStates import *

class Field():
    def __init__(self, logger):

        # [A_X,A_Y, B_X,B_Y, BALL_AT_A]
        # [int,int, int,int,  boolean ]
        # self.state = [0,0,FIELD_WIDTH-1,FIELD_HEIGHT-1,1]
        self.__logger = logger
        self.initField()

        self.gamesPlayed = 1

    def initField(self):
        self.state = [0]*5

        self.state[A_X_IND] = 7
        self.state[A_Y_IND] = 3
        self.state[B_X_IND] = 2
        self.state[B_Y_IND] = 4

        if (random.random() <= 0.5):
            self.state[HAS_BALL_INDEX] = BALL_AT_B
        else:
            self.state[HAS_BALL_INDEX] = BALL_AT_A

        self.field = [[EMPTY_CELL_CHAR for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)] 

        for point in GATEA_POS:
            self.field[point[0]][point[1]] = GATEA_CHAR

        for point in GATEB_POS:
            self.field[point[0]][point[1]] = GATEB_CHAR

    def getState(self):
        return self.state        

    def drawA(self, field):
        if (self.hasBall('a')):
            field[self.state[A_Y_IND]][self.state[A_X_IND]] = 'A'
        else:
            field[self.state[A_Y_IND]][self.state[A_X_IND]] = 'a'


    def drawB(self, field):
        if (self.hasBall('b')):
            field[self.state[B_Y_IND]][self.state[B_X_IND]] = 'B'
        else:
            field[self.state[B_Y_IND]][self.state[B_X_IND]] = 'b'


    def moveTo(self, direction, player = 'b'):
        if (MOVE_UP == direction or 'u' == direction or 'up' == direction):
            return self.moveUp(player)
        elif (MOVE_DOWN == direction or 'd' == direction or 'down' == direction):
            return self.moveDown(player)
        elif (MOVE_LEFT == direction or 'l' == direction or 'left' == direction):
            return self.moveLeft(player)
        elif (MOVE_RIGHT == direction or 'r' == direction or 'right' == direction):
            return self.moveRight(player)

        return NO_REWARD


    def moveUp(self, player = 'b'):
        playerYIndex = A_Y_IND
        
        if (self.isBPlayer(player)):
            playerYIndex = B_Y_IND

        if (self.state[playerYIndex] > 0):
            self.state[playerYIndex] -= 1

            if (self.standingAboveTheOther(player)):
                self.state[playerYIndex] += 1
                self.passTheBall(player)

        return NO_REWARD

    def moveDown(self, player = 'b'):
        playerYIndex = A_Y_IND
        
        if (self.isBPlayer(player)):
            playerYIndex = B_Y_IND

        if (self.state[playerYIndex] < FIELD_HEIGHT-1):
            self.state[playerYIndex] += 1

            if (self.standingAboveTheOther(player)):
                self.state[playerYIndex] -= 1
                self.passTheBall(player)

        return NO_REWARD

    def moveLeft(self, player = 'b'):
        playerXIndex = A_X_IND
        
        if (self.isBPlayer(player)):
            playerXIndex = B_X_IND

        if (self.state[playerXIndex] > 1):
            self.state[playerXIndex] -= 1

            if (self.standingAboveTheOther(player)):
                self.state[playerXIndex] += 1
                self.passTheBall(player)

        elif (self.isPlayerInFrontOfGate(player) and self.hasBall(player)):
            #end of game
            # self.setGoal(player)
            return GOAL_REWARD

        return NO_REWARD

    def moveRight(self, player = 'b'):
        playerXIndex = A_X_IND
        
        if (self.isBPlayer(player)):
            playerXIndex = B_X_IND

        if (self.state[playerXIndex] < FIELD_WIDTH - 2):
            self.state[playerXIndex] += 1

            if (self.standingAboveTheOther(player)):
                self.state[playerXIndex] -= 1
                self.passTheBall(player)

        elif (self.isPlayerInFrontOfGate(player) and self.hasBall(player)):
            #end of game
            # self.setGoal(player)
            return GOAL_REWARD

        return NO_REWARD

    def isPlayerInFrontOfGate(self, player = 'b'):
        
        if (self.isBPlayer(player)):
            for point in GATEA_POS:
                if (self.state[B_Y_IND] == point[0] and abs(self.state[B_X_IND] - point[1]) <= 1):
                    return True
        else:
            for point in GATEB_POS:
                if (self.state[A_Y_IND] == point[0] and abs(self.state[A_X_IND] - point[1]) <= 1):
                    return True

        return False

    def standingAboveTheOther(self, player = 'b'):
        if (self.state[B_Y_IND] == self.state[A_Y_IND] and
            self.state[B_X_IND] == self.state[A_X_IND]):
            return True
        return False

    def passTheBall(self, player):
        if (self.hasBall(player)):
            self.state[HAS_BALL_INDEX] = (self.state[HAS_BALL_INDEX] + 1) % 2

    def hasBall(self, player):
        if (self.isBPlayer(player)):
            return BALL_AT_B == self.state[HAS_BALL_INDEX]
        else:
            return BALL_AT_A == self.state[HAS_BALL_INDEX]

    def getFieldCellByPlayerPos(self, player):
        if (self.isBPlayer(player)):
            return self.field[self.state[B_Y_IND]][self.state[B_X_IND]]
        else:
            return self.field[self.state[A_Y_IND]][self.state[A_X_IND]]

    def setGoal(self, player):
        if (self.isBPlayer(player)):
            self.field[self.state[B_Y_IND]][self.state[B_X_IND]+1] = '_'
        else:
            self.field[self.state[A_Y_IND]][self.state[A_X_IND]-1] = '_'

    # def inGate(self, player):
    #     if (self.isBPlayer(player)):
    #         return GATEA_CHAR == self.getFieldCellByPlayerPos(player)
    #     else:
    #         return GATEB_CHAR == self.getFieldCellByPlayerPos(player)

    def isBPlayer(self, player):
        if ('b' == player or 'B' == player):
            return True
        return False


    def test(self, Q, opponentStrategy, batchSize = 100):
        return self.train(Q, opponentStrategy, batchSize, False, True, False)

    def train(self, Q, opponentStrategy, batchSize = 100, trainMode = True, printStat = False, printGame = False):
        
        a_wins_counter = 0
        b_wins_counter = 0

        if (trainMode):
            percentageOfExploitation = 0.95
        else:
            percentageOfExploitation = 1.0

        # for game_number in xrange(1,batchSize):
        game_number = 1
        while game_number < batchSize:

            moveCounter = 0

            self.initField()

            if (trainMode):
                self.gamesPlayed += 1

            while (True):

                if (moveCounter > FIELD_WIDTH * FIELD_HEIGHT):
                    # print "moveCounter ", moveCounter
                    break

                beforeMoveFieldState = copy.deepcopy(self.getState())

                if (printGame):
                    print self

                if (random.random() <= 0.5):
                    directionB, rewardB = self.bPlays(Q, beforeMoveFieldState, percentageOfExploitation)

                    if (printGame):
                        print self

                    directionA, rewardA = self.aPlays(opponentStrategy, beforeMoveFieldState)
                else:
                    directionA, rewardA = self.aPlays(opponentStrategy, beforeMoveFieldState)

                    if (printGame):
                        print self

                    directionB, rewardB = self.bPlays(Q, beforeMoveFieldState, percentageOfExploitation)


                if (printGame):
                    print self

                moveCounter += 1

                # For test only
                if (trainMode):
                    similarStatesList = getSimilarStates(beforeMoveFieldState, directionB, self.getState())

                    reward = Q.getRewardUpdate(rewardA, rewardB)

                    expectedError = Q.calculateError(reward, beforeMoveFieldState, directionB, self.getState())
                    # Q.update(beforeMoveFieldState, directionB, self.getState(), reward, 1.0, expectedError)

                    for stateAction in similarStatesList:
                        if (USE_DECAY):
                            Q.update(
                                stateAction[0],
                                stateAction[1],
                                self.getState(),
                                reward,
                                stateAction[2] / (game_number ** 0.1),
                                expectedError
                            )
                        else:
                            Q.update(
                                stateAction[0],
                                stateAction[1],
                                self.getState(),
                                reward,
                                stateAction[2],
                                expectedError
                            )

                if (rewardA > 0):
                    a_wins_counter += 1
                    # print " :  A wins  A vs B ", (game_number - b_wins_counter)*1.0 / game_number , " vs ", b_wins_counter*1.0 / game_number, " times of ", game_number
                    break

                if (rewardB > 0):
                    b_wins_counter += 1
                    # print " :  B wins  A vs B ", (game_number - b_wins_counter)*1.0 / game_number , " vs ", b_wins_counter*1.0 / game_number, " times of ", game_number
                    break

            # Q.alpha = ALPHA
            if (USE_DECAY):
                Q.alpha = ALPHA / (game_number ** 0.1)
            else:
                Q.alpha = ALPHA
            # Q.alpha = ALPHA / (self.gamesPlayed ** 0.1)

            # if (trainMode):
                # print self.gamesPlayed, " Q.alpha", Q.alpha

            game_number += 1

        if printStat:
            if (a_wins_counter + b_wins_counter) > 0:
                self.__logger.log(float(b_wins_counter) / (a_wins_counter + b_wins_counter))
                # self.__logger.log("A vs B {a_wins} vs {b_wins} draw: {draw}".format(
                #     a_wins=(((a_wins_counter)*1.0) / (a_wins_counter+b_wins_counter)),
                #     b_wins=((b_wins_counter*1.0) / (a_wins_counter+b_wins_counter)),
                #     draw=((game_number - (a_wins_counter+b_wins_counter))*1.0 / batchSize)
                # ))
            else:
                self.__logger.log(0)
                # self.__logger.log("A vs B 0 vs 0 draw: 1.0")

        if (a_wins_counter + b_wins_counter) > 0:
            return float(b_wins_counter) / (a_wins_counter + b_wins_counter)
        else:
            return 0.0


    def bPlays(self, strategy, beforeMoveFieldState, percentageOfExploitation):

        directionB = strategy.getNextAction(beforeMoveFieldState, percentageOfExploitation)

        return directionB, self.moveTo(directionB,'b')

    def aPlays(self, strategy, beforeMoveFieldState):

        directionA = strategy.getBestMove(beforeMoveFieldState, 0.0)
        # directionA = random.choice([MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, DONT_MOVE])

        return directionA, self.moveTo(directionA,'a')


    def __str__(self):
        output = '----------\n'

        tempField = copy.deepcopy(self.field)

        self.drawA(tempField)
        self.drawB(tempField)

        for x in xrange(len(tempField)-1):
            output += str(tempField[x]) + '\n'

        #add the last row without \n
        output += str(tempField[len(tempField)-1])

        return output
        

