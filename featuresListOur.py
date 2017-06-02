from constans import *
import copy

# state[0] = A_X_IND
# state[1] = A_Y_IND
# state[2] = B_X_IND
# state[3] = B_Y_IND
# state[4] = HAS_BALL_INDEX

# BALL_AT_A = 1
# BALL_AT_B = 0

def getFeaturesList(state, action):

    tempList = []

    p1 = False
    p2 = False


    if (BALL_AT_B == state[HAS_BALL_INDEX]):
        multiplier = 1.0
        
        attacker = 'b'
        defender = 'a'
        attacker_x_index = B_X_IND
        attacker_y_index = B_Y_IND

        defender_x_index = A_X_IND
        defender_y_index = A_Y_IND

        attackerGatePos = GATEA_POS
        defenderGatePos = GATEB_POS
    else:
        multiplier = -1.0

        attacker = 'a'
        defender = 'b'
        attacker_x_index = A_X_IND
        attacker_y_index = A_Y_IND

        defender_x_index = B_X_IND
        defender_y_index = B_Y_IND

        attackerGatePos = GATEB_POS
        defenderGatePos = GATEA_POS


    attackerHDistanceToGate     = abs(state[attacker_x_index] - attackerGatePos[0][1]) * 1.0 / (FIELD_WIDTH - 2)
    attackerVDistanceToGate     = (state[attacker_y_index] - attackerGatePos[0][0] + (FIELD_HEIGHT-1)) * 1.0 / (2 * (FIELD_HEIGHT-1))

    attackerDistanceToGate         = (abs(state[attacker_y_index] - attackerGatePos[0][0]) + abs(state[attacker_x_index] - attackerGatePos[0][1])) * 1.0 / (FIELD_HEIGHT + FIELD_WIDTH - 2)
    defenderDistanceToGate         = (abs(state[defender_y_index] - attackerGatePos[0][0]) + abs(state[defender_x_index] - attackerGatePos[0][1])) * 1.0 / (FIELD_HEIGHT + FIELD_WIDTH - 2)

    distanceToOpponent     = (abs(state[attacker_y_index] - state[defender_y_index])  + abs(state[attacker_x_index] - state[defender_x_index])) * 1.0 / (FIELD_WIDTH - 2)

    distanceHToOpponent     = (state[attacker_x_index] - state[defender_x_index] + (FIELD_WIDTH - 2)) * 1.0 / (2 * (FIELD_WIDTH - 2))
    distanceVToOpponent     = (state[attacker_y_index] - state[defender_y_index] + (FIELD_HEIGHT-1)) * 1.0 / (2 * (FIELD_HEIGHT-1))



    if (attackerDistanceToGate < defenderDistanceToGate):
        p1 = true

    if (distanceToOpponent <= 2):
        p2 = true


    for i in xrange(0,5):

        if (action == i):
            if (p1 and not p2):
                tempList.append(multiplier * 1)
                tempList.append(multiplier * attackerHDistanceToGate)
                tempList.append(multiplier * attackerVDistanceToGate)
                tempList.append(multiplier * attackerHDistanceToGate * attackerVDistanceToGate)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)

                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)


            if (p1 and p2):
                tempList.append(1)
                tempList.append(multiplier * attackerHDistanceToGate)
                tempList.append(multiplier * attackerVDistanceToGate)
                tempList.append(multiplier * attackerHDistanceToGate * attackerVDistanceToGate)
                tempList.append(multiplier * distanceHToOpponent)
                tempList.append(multiplier * distanceVToOpponent)
                tempList.append(0)

                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)

            if (not p1 and not p2):
                tempList.append(1)
                tempList.append(multiplier * attackerHDistanceToGate)
                tempList.append(0)
                tempList.append(multiplier * attackerHDistanceToGate * attackerVDistanceToGate)
                tempList.append(multiplier * distanceHToOpponent)
                tempList.append(multiplier * distanceVToOpponent)
                tempList.append(0)

                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)
                tempList.append(0)

            if (not p1 and p2):
                tempList.append(0)
                tempList.append(multiplier * attackerHDistanceToGate)
                tempList.append(multiplier * attackerVDistanceToGate)
                tempList.append(multiplier * attackerHDistanceToGate * attackerVDistanceToGate)
                tempList.append(0)
                tempList.append(0)
                tempList.append(multiplier * isPlayerInFrontOfGate(state, defender))

                if (state[attacker_x_index] - state[defender_x_index] == 1 and state[attacker_y_index] - state[defender_y_index] == 0):
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 2 and state[attacker_y_index] - state[defender_y_index] == 0):
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 1 and state[attacker_y_index] - state[defender_y_index] == 1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 1 and state[attacker_y_index] - state[defender_y_index] == -1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 0 and state[attacker_y_index] - state[defender_y_index] == 1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 0 and state[attacker_y_index] - state[defender_y_index] == -1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 0 and state[attacker_y_index] - state[defender_y_index] == -2):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == 0 and state[attacker_y_index] - state[defender_y_index] == 2):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == -1 and state[attacker_y_index] - state[defender_y_index] == 0):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == -1 and state[attacker_y_index] - state[defender_y_index] == -1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)
                    tempList.append(0)


                elif (state[attacker_x_index] - state[defender_x_index] == -1 and state[attacker_y_index] - state[defender_y_index] == 1):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)
                    tempList.append(0)

                elif (state[attacker_x_index] - state[defender_x_index] == -2 and state[attacker_y_index] - state[defender_y_index] == 0):
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(0)
                    tempList.append(1)

        else:
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)

            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)
            tempList.append(0)




    return tempList

def isPlayerInFrontOfGate(state, player = 'b'):
    
    if ('b' == player):
        for point in GATEA_POS:
            if (state[B_Y_IND] == point[0] and abs(state[B_X_IND] - point[1]) <= 1):
                return 1.0
    else:
        for point in GATEB_POS:
            if (state[A_Y_IND] == point[0] and abs(state[A_X_IND] - point[1]) <= 1):
                return 1.0

    return 0.0

# def getFeaturesList(state, action):

#     tempList = []

#     tempList.append(abs(state[A_X_IND] - state[B_X_IND]))
#     tempList.append(abs(state[A_Y_IND] - state[B_Y_IND]))

#     if (BALL_AT_A == state[HAS_BALL_INDEX]):
#         tempList.append(abs(state[A_X_IND] - state[B_X_IND]) + abs(state[A_Y_IND] - state[B_Y_IND]))
#         tempList.append(0)
#     else:
#         tempList.append(0)
#         tempList.append(abs(state[B_Y_IND] - GATEA_POS[0][0]) + abs(state[B_X_IND] - GATEA_POS[0][1]))


#     tempList.append(1 if action == 0 else 0)
#     tempList.append(1 if action == 1 else 0)
#     tempList.append(1 if action == 2 else 0)
#     tempList.append(1 if action == 3 else 0)
#     tempList.append(1 if action == 4 else 0)

#     tempList.append(state[HAS_BALL_INDEX])

#     return tempList