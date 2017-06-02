from constans import *
import copy

# state[0] = A_X_IND
# state[1] = A_Y_IND
# state[2] = B_X_IND
# state[3] = B_Y_IND
# state[4] = HAS_BALL_INDEX

# BALL_AT_A = 1
# BALL_AT_B = 0

def addVerticalSimetrySim(currentState, currentAction, nextState, similarityVal = 1.0):

    tempCurState = copy.deepcopy(currentState)

    tempCurState[A_Y_IND] = (FIELD_HEIGHT-1) - tempCurState[A_Y_IND]
    tempCurState[B_Y_IND] = (FIELD_HEIGHT-1) - tempCurState[B_Y_IND]

    if (MOVE_UP == currentAction):
        currentAction = MOVE_DOWN

    if (MOVE_DOWN == currentAction):
        currentAction = MOVE_UP

    return [tempCurState, currentAction, similarityVal*0.9]

def addHorizontalSimetrySim(currentState, currentAction, nextState, similarityVal = 1.0):

    tempCurState = copy.deepcopy(currentState)
    tempCurAction = copy.deepcopy(currentAction)

    #Swap the position
    tempCurState[A_X_IND] = (FIELD_WIDTH-1) - tempCurState[A_X_IND]
    tempCurState[B_X_IND] = (FIELD_WIDTH-1) - tempCurState[B_X_IND]

    #Swap identities

    bTempPosX = copy.deepcopy(tempCurState[B_X_IND])
    bTempPosY = copy.deepcopy(tempCurState[B_Y_IND])

    tempCurState[B_X_IND] = copy.deepcopy(tempCurState[A_X_IND])
    tempCurState[B_Y_IND] = copy.deepcopy(tempCurState[A_Y_IND])

    tempCurState[A_X_IND] = copy.deepcopy(bTempPosX)
    tempCurState[A_Y_IND] = copy.deepcopy(bTempPosY)


    #Swap the action
    if (MOVE_LEFT == tempCurAction):
        tempCurAction = MOVE_RIGHT
    elif (MOVE_RIGHT == tempCurAction):
        tempCurAction = MOVE_LEFT

    #Swap ball state
    tempCurState[HAS_BALL_INDEX] = (tempCurState[HAS_BALL_INDEX] + 1) % 2

    return [tempCurState, tempCurAction, -1 * similarityVal * 0.8]

def addDefenceSim(currentState, currentAction, nextState, similarityVal = 1.0):

    tempCurState = copy.deepcopy(currentState)
    tempCurAction = copy.deepcopy(currentAction)

    similarStatesList = []

    if (tempCurState[A_X_IND] - tempCurState[B_X_IND] == 1):
        for x1 in [-1,0,1]:
            for y1 in [-1,0,1]:

                tempTempCurState = copy.deepcopy(currentState)

                tempTempCurState[A_X_IND] += x1
                tempTempCurState[B_X_IND] += x1


                tempTempCurState[A_Y_IND] += y1
                tempTempCurState[B_Y_IND] += y1

                if (tempTempCurState[A_X_IND] < 1 or tempTempCurState[A_X_IND] > (FIELD_WIDTH-2) or
                    tempTempCurState[A_X_IND] < 1 or tempTempCurState[A_X_IND] > (FIELD_WIDTH-2)):
                    continue

                if (tempTempCurState[A_Y_IND] < 0 or tempTempCurState[A_Y_IND] > (FIELD_HEIGHT-1) or
                    tempTempCurState[A_Y_IND] < 0 or tempTempCurState[A_Y_IND] > (FIELD_HEIGHT-1)):
                    continue

                similarStatesList.append([tempTempCurState, tempCurAction, similarityVal * 0.5])

                
    return similarStatesList

def addDefence2Sim(currentState, currentAction, nextState, similarityVal = 1.0):

    tempCurState = copy.deepcopy(currentState)
    tempCurAction = copy.deepcopy(currentAction)

    similarStatesList = []

    if (BALL_AT_B == tempCurState[HAS_BALL_INDEX]):
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


    attackerDistanceToGate         = (abs(tempCurState[attacker_y_index] - attackerGatePos[0][0]) + abs(tempCurState[attacker_x_index] - attackerGatePos[0][1])) * 1.0 / (FIELD_HEIGHT + FIELD_WIDTH - 2)
    defenderDistanceToGate         = (abs(tempCurState[defender_y_index] - attackerGatePos[0][0]) + abs(tempCurState[defender_x_index] - attackerGatePos[0][1])) * 1.0 / (FIELD_HEIGHT + FIELD_WIDTH - 2)


    if (attackerDistanceToGate < defenderDistanceToGate):
        if (tempCurState[A_X_IND] - tempCurState[B_X_IND] == 1):
            for x1 in xrange(-FIELD_WIDTH+1,FIELD_WIDTH-1):
                for y1 in xrange(-FIELD_HEIGHT+1,FIELD_HEIGHT-1):

                    tempTempCurState = copy.deepcopy(currentState)

                    tempTempCurState[A_X_IND] += x1
                    tempTempCurState[B_X_IND] += x1

                    if (tempTempCurState[A_X_IND] < 1 or tempTempCurState[A_X_IND] > (FIELD_WIDTH-2) or
                        tempTempCurState[A_X_IND] < 1 or tempTempCurState[A_X_IND] > (FIELD_WIDTH-2)):
                        tempTempCurState[A_X_IND] -= x1
                        tempTempCurState[B_X_IND] -= x1
                        pass
                    else:
                        similarStatesList.append([tempTempCurState, tempCurAction, similarityVal * 0.5])


                    tempTempCurState[A_Y_IND] += y1
                    tempTempCurState[B_Y_IND] += y1

                    if (tempTempCurState[A_Y_IND] < 0 or tempTempCurState[A_Y_IND] > (FIELD_HEIGHT-1) or
                        tempTempCurState[A_Y_IND] < 0 or tempTempCurState[A_Y_IND] > (FIELD_HEIGHT-1)):
                        tempTempCurState[A_Y_IND] -= y1
                        tempTempCurState[B_Y_IND] -= y1
                        pass
                    else:
                        similarStatesList.append([tempTempCurState, tempCurAction, similarityVal * 0.5])
                    
    return similarStatesList


def addRepSim(currentState, currentAction, nextState):
    tempCurState = copy.deepcopy(currentState)

    similarStatesList = []

    for x1 in [-1,0,1]:
        for y1 in [-1,0,1]:
            tempCurState = copy.deepcopy(currentState)

            tempCurState[0] += x1

            if (tempCurState[0] < 1 or tempCurState[0] > 5):
                continue
                
            tempCurState[1] += y1

            if (tempCurState[1] < 0 or tempCurState[1] > 3):
                continue
            
            if (0 == x1 and 0 == y1):
                continue

            simVal = 0.1

            if (0 != x1 and 0 != y1):
                simVal = 0.01

            similarStatesList.append([tempCurState, currentAction, simVal])

    # for x1 in [-1,0,1]:
    #     for y1 in [-1,0,1]:
    #         for x2 in [-1,0,1]:
    #             for y2 in [-1,0,1]:
    #                 tempCurState = copy.deepcopy(currentState)

    #                 tempCurState[0] += x1

    #                 if (tempCurState[0] < 1 or tempCurState[0] > 5):
    #                     continue
                        
    #                 tempCurState[1] += y1

    #                 if (tempCurState[1] < 0 or tempCurState[1] > 3):
    #                     continue

    #                 tempCurState[2] += x2

    #                 if (tempCurState[2] < 1 or tempCurState[2] > 5):
    #                     continue
                        
    #                 tempCurState[3] += y2


    #                 if (tempCurState[3] < 0 or tempCurState[3] > 3):
    #                     continue

    #                 similarStatesList.append([tempCurState, currentAction, 0.7 * 0.7])

    return similarStatesList

def addTransitionSim(currentState, currentAction, nextState, similarityVal = 1.0):

    tempCurState = copy.deepcopy(currentState)

    similarStatesList = []

    myX = tempCurState[2]
    myY = tempCurState[3]

    # myNextX = nextState[2]
    # myNextY = nextState[3]

    opponentX = tempCurState[0]
    opponentY = tempCurState[1]

    if (tempCurState[4] == BALL_AT_A):
        if (opponentY < myY and opponentX < myX):
            if (MOVE_UP == currentAction):
                similarStatesList.append([tempCurState, MOVE_LEFT, similarityVal * 0.5])
            elif (MOVE_LEFT == currentAction):
                similarStatesList.append([tempCurState, MOVE_UP, similarityVal * 0.5])
        elif (opponentY < myY and opponentX > myX):
            if (MOVE_UP == currentAction):
                similarStatesList.append([tempCurState, MOVE_RIGHT, similarityVal * 0.5])
            elif (MOVE_RIGHT == currentAction):
                similarStatesList.append([tempCurState, MOVE_UP, similarityVal * 0.5])
        elif (opponentY > myY and opponentX > myX):
            if (MOVE_DOWN == currentAction):
                similarStatesList.append([tempCurState, MOVE_RIGHT, similarityVal * 0.5])
            elif (MOVE_RIGHT == currentAction):
                similarStatesList.append([tempCurState, MOVE_DOWN, similarityVal * 0.5])
        elif (opponentY > myY and opponentX < myX):
            if (MOVE_DOWN == currentAction):
                similarStatesList.append([tempCurState, MOVE_LEFT, similarityVal * 0.5])
            elif (MOVE_LEFT == currentAction):
                similarStatesList.append([tempCurState, MOVE_DOWN, similarityVal * 0.5])

        # if (GATEB_POS[0][0] == myX || GATEB_POS[1][0] == myX):
    else:
        if (GATEA_POS[0][0] > myY and myX < FIELD_WIDTH-2):
            if (MOVE_DOWN == currentAction):
                similarStatesList.append([tempCurState, MOVE_RIGHT, similarityVal * 0.5])
            elif (MOVE_RIGHT == currentAction):
                similarStatesList.append([tempCurState, MOVE_DOWN, similarityVal * 0.5])
        elif (GATEA_POS[1][0] < myY and myX < FIELD_WIDTH-2):
            if (MOVE_DOWN == currentAction):
                similarStatesList.append([tempCurState, MOVE_RIGHT, similarityVal * 0.5])
            elif (MOVE_RIGHT == currentAction):
                similarStatesList.append([tempCurState, MOVE_DOWN, similarityVal * 0.5])


    return similarStatesList

def getSimilarStates(currentState, currentAction, nextState):
    similarStatesList = []

    tempCurState = copy.deepcopy(currentState)
    tempNextState = copy.deepcopy(nextState)

    similarStatesList.append([tempCurState, currentAction, 1.0])

    if (USE_SIMILARITIES):
        tempSims1 = [addVerticalSimetrySim(tempCurState, currentAction, tempNextState)]
        tempSims2 = addTransitionSim(tempCurState, currentAction, tempNextState)
        tempSims3 = [addHorizontalSimetrySim(tempCurState, currentAction, tempNextState)]
        tempSims4 = addDefenceSim(tempCurState, currentAction, tempNextState)
        tempSims5 = addDefence2Sim(tempCurState, currentAction, tempNextState)

        similarStatesList.extend(tempSims1)
        similarStatesList.extend(tempSims2)
        similarStatesList.extend(tempSims3)
        similarStatesList.extend(tempSims4)
        similarStatesList.extend(tempSims5)


        # for sim in tempSims1:

        #     tempRegSims2 = addTransitionSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims3 = [addHorizontalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims4 = addDefenceSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims5 = addDefence2Sim(sim[0], sim[1], sim[0], sim[2])

        #     similarStatesList.extend(tempRegSims2)
        #     similarStatesList.extend(tempRegSims3)
        #     similarStatesList.extend(tempRegSims4)
        #     similarStatesList.extend(tempRegSims5)


        # for sim in tempSims2:

        #     tempRegSims1 = [addVerticalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims3 = [addHorizontalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims4 = addDefenceSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims5 = addDefence2Sim(sim[0], sim[1], sim[0], sim[2])

        #     similarStatesList.extend(tempRegSims1)
        #     similarStatesList.extend(tempRegSims3)
        #     similarStatesList.extend(tempRegSims4)
        #     similarStatesList.extend(tempRegSims5)


        # for sim in tempSims3:

        #     tempRegSims1 = [addVerticalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims2 = addTransitionSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims4 = addDefenceSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims5 = addDefence2Sim(sim[0], sim[1], sim[0], sim[2])

        #     similarStatesList.extend(tempRegSims1)
        #     similarStatesList.extend(tempRegSims2)
        #     similarStatesList.extend(tempRegSims4)
        #     similarStatesList.extend(tempRegSims5)


        # for sim in tempSims4:

        #     tempRegSims1 = [addVerticalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims2 = addTransitionSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims3 = [addHorizontalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims5 = addDefence2Sim(sim[0], sim[1], sim[0], sim[2])

        #     similarStatesList.extend(tempRegSims1)
        #     similarStatesList.extend(tempRegSims2)
        #     similarStatesList.extend(tempRegSims3)
        #     similarStatesList.extend(tempRegSims5)


        # for sim in tempSims5:

        #     tempRegSims1 = [addVerticalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims2 = addTransitionSim(sim[0], sim[1], sim[0], sim[2])
        #     tempRegSims3 = [addHorizontalSimetrySim(sim[0], sim[1], sim[0], sim[2])]
        #     tempRegSims4 = addDefenceSim(sim[0], sim[1], sim[0], sim[2])

        #     similarStatesList.extend(tempRegSims1)
        #     similarStatesList.extend(tempRegSims2)
        #     similarStatesList.extend(tempRegSims3)
        #     similarStatesList.extend(tempRegSims4)




        # for x in repList:
        #     similarStatesList.append(addVerticalSimetrySim(x[0],x[1],x[0],x[2]))

        # similarStatesList.append(addVerticalSimetrySim(addHorizontalSimetrySim(tempCurState, currentAction, tempNextState)))


    # repList = addRepSim(tempCurState, currentAction, tempNextState)

    # for x in repList:
    #     similarStatesList.append(addVerticalSimetrySim(x[0],x[1],x[0],x[2]))

    # similarStatesList.extend(repList)





    #add your states here

    # print len(similarStatesList)
    return similarStatesList