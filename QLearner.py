#!/usr/bin/env python2

import random
from constans import *
from shaping_manager import ShapingManager

from userStates import *

class QLearner():
    def __init__(self, player, ownStatesOnly = True):
        self.player = player

        self.ownStatesOnly = ownStatesOnly

        self.Q = {}

        self.alpha = ALPHA

        self.iHaveABall = BALL_AT_B
        self.opponentGatePos = GATEA_POS
        self.myXPositionIndex = B_X_IND
        self.myYPositionIndex = B_Y_IND
        self.opponentXPositionIndex = A_X_IND
        self.opponentYPositionIndex = A_Y_IND

        if ('a' == self.player or 'A' == self.player):
            self.iHaveABall = BALL_AT_A
            self.opponentGatePos = GATEB_POS
            self.myXPositionIndex = A_X_IND
            self.myYPositionIndex = A_Y_IND
            self.opponentXPositionIndex = B_X_IND
            self.opponentYPositionIndex = B_Y_IND

        self.shaping_manager = ShapingManager()

    def getValue(self, state, action):

        if (self.ownStatesOnly):
            state = str(state)

            if (not state in self.Q):
                return 0.0

            if (len(self.Q[state]) <= action):
                return 0.0

            return self.Q[state][action]

        else:

            userState = getUserState(state, action)
            stateStr = str(userState)

            if (not stateStr in self.Q):
                return 0.0

            if (len(self.Q[stateStr]) <= action):
                return 0.0

            return self.Q[stateStr][action]

            

    def setValue(self, state, action, value):

        if (self.ownStatesOnly):
            state = str(state)

            if (not state in self.Q):
                self.Q[state] = [0.0]*ACTIONS_NUMBER

            if (action >= ACTIONS_NUMBER):
                print "action ", action, " is out of range: ", ACTIONS_NUMBER-1
                return

            self.Q[state][action] = value
        else:
            userState = getUserState(state, action)
            stateStr = str(userState)

            if (not stateStr in self.Q):
                self.Q[stateStr] = [0.0]*ACTIONS_NUMBER

            if (action >= ACTIONS_NUMBER):
                print "action ", action, " is out of range: ", ACTIONS_NUMBER-1
                return

            self.Q[stateStr][action] = value

    def update(self, state, action, new_state, reward, similarity):

        oldQValue = self.getValue(state, action)

        learningRate = self.alpha * similarity

        newQValue = oldQValue + learningRate * self.calculateError(reward, state, action, new_state)

        self.setValue(state, action, newQValue)

    def update(self, state, action, new_state, reward, similarity, expectedError):

        oldQValue = self.getValue(state, action)

        learningRate = self.alpha * similarity

        newQValue = oldQValue + learningRate * expectedError

        self.setValue(state, action, newQValue)

    def calculateError(self, reward, state, action, new_state):
        return \
            reward \
            + self.getShapedReward(state, new_state) \
            + self.shaping_manager.get_shaping_reward(state, action, new_state) \
            + DISCOUNT_FACTOR * self.getValue(new_state, self.getBestAction(new_state)) \
            - self.getValue(state, action)

    def getBestActionMulti(self, state):
        bestActionValue = float('-inf')
        bestAction = 0

        bestActionArr = []        

        for nextAction in xrange(0, ACTIONS_NUMBER):
            nextActionValue = self.getValue(state, nextAction)

            if (bestActionValue < nextActionValue):
                bestActionValue = nextActionValue
                bestAction = nextAction
                bestActionArr = []
                bestActionArr.append(nextAction)
            elif (bestActionValue == nextActionValue):
                bestActionArr.append(nextAction)

        return bestActionArr[random.randint(0,len(bestActionArr)-1)]

    def getBestAction(self, state):
        bestActionValue = float('-inf')
        bestAction = 0

        for nextAction in xrange(0, ACTIONS_NUMBER):
            nextActionValue = self.getValue(state, nextAction)

            if (bestActionValue < nextActionValue):
                bestActionValue = nextActionValue
                bestAction = nextAction

        # return bestActionArr[random.randint(0,len(bestActionArr)-1)]
        return bestAction

    def getRewardUpdate(self, rewardA, rewardB):
        if (rewardA > 0):
            return -1 * GOAL_REWARD

        if (rewardB > 0):
            return GOAL_REWARD

        return 0.0

    def getNextAction(self, state, percentageOfExploitation = 0.95):
        if random.random() <= percentageOfExploitation:
            return self.getBestAction(state)
        else:
            return random.randint(0, ACTIONS_NUMBER-1)

    def __str__(self):
        # output = '----------\n'
        #
        # for state in self.Q:
        #     output += str(state) + ' -> ' + str(self.Q[state]) + '\n'
        #
        # return output
        return ""

    def getShapedReward(self, state, new_state):
        return DISCOUNT_FACTOR * self.potentialPhi(new_state) - self.potentialPhi(state)

    def potentialPhi(self, state):
        myX = state[self.myXPositionIndex]
        myY = state[self.myYPositionIndex]

        opponentX = state[self.opponentXPositionIndex]
        opponentY = state[self.opponentYPositionIndex]

        if (state[HAS_BALL_INDEX] == self.iHaveABall):
            point = self.opponentGatePos[random.randint(0, len(self.opponentGatePos)-1)]

            distanceFromOpponentGate = abs(point[0] - myY) + abs(point[1] - myX)

            return 1.0 / distanceFromOpponentGate
        else:
            point = [opponentY,opponentX]

            distanceFromOpponent = abs(point[0] - myY) + abs(point[1] - myX)

            return -1.0 * distanceFromOpponent / (FIELD_WIDTH+FIELD_HEIGHT-3)