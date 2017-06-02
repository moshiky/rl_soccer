#!/usr/bin/env python2

import random
from constans import *

class OpponentStrategy():
    def __init__(self, player):
        self.player = player
        if ('b' == player or 'B' == player):
            self.iHaveABall = BALL_AT_B
            self.opponentGatePos = GATEA_POS
            self.myXPositionIndex = B_X_IND
            self.myYPositionIndex = B_Y_IND
            self.opponentXPositionIndex = A_X_IND
            self.opponentYPositionIndex = A_Y_IND
        else:
            self.iHaveABall = BALL_AT_A
            self.opponentGatePos = GATEB_POS
            self.myXPositionIndex = A_X_IND
            self.myYPositionIndex = A_Y_IND
            self.opponentXPositionIndex = B_X_IND
            self.opponentYPositionIndex = B_Y_IND


    def getBestMove(self,state, random_move = 0.0):

        if (random.random() < random_move):
            return random.randint(0,ACTIONS_NUMBER-1)

        myX = state[self.myXPositionIndex]
        myY = state[self.myYPositionIndex]

        opponentX = state[self.opponentXPositionIndex]
        opponentY = state[self.opponentYPositionIndex]

        if (state[HAS_BALL_INDEX] == self.iHaveABall):
            point = self.opponentGatePos[random.randint(0, len(self.opponentGatePos)-1)]

            if (random.random() <= 1.0):
                if (point[0] < myY):
                    return MOVE_UP
                elif (point[0] > myY):
                    return MOVE_DOWN
                elif (point[1] > myX):
                    return MOVE_RIGHT
                else:
                    return MOVE_LEFT
            else:
                if (point[1] > myX):
                    return MOVE_RIGHT
                elif (point[1] < myX):
                    return MOVE_LEFT
                elif (point[0] < myY):
                    return MOVE_UP
                else:
                    return MOVE_DOWN
        else:
            point = [opponentY,opponentX]

            if (random.random() <= 1.0):
                if (point[0] < myY):
                    return MOVE_UP
                elif (point[0] > myY):
                    return MOVE_DOWN
                elif (point[1] > myX):
                    return MOVE_RIGHT
                else:
                    return MOVE_LEFT
            else:
                if (point[1] > myX):
                    return MOVE_RIGHT
                elif (point[1] < myX):
                    return MOVE_LEFT
                elif (point[0] < myY):
                    return MOVE_UP
                else:
                    return MOVE_DOWN

        return random.randint(0,ACTIONS_NUMBER-1)