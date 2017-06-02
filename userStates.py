from constans import *
import copy

# The x position of player A
# state[A_X_IND]

# The y position of player A
# state[A_Y_IND]

# The x position of player A
# state[B_X_IND]

# The y position of player B
# state[B_Y_IND]

# Who has a ball (two possible values): 
    # BALL_AT_A = 1
    # BALL_AT_B = 0
# state[HAS_BALL_INDEX]

# Expected output: 
#     your implementation of state
def getUserState(originalState, action):

    x = 0
    y = 0

    # if (BALL_AT_B == originalState[HAS_BALL_INDEX]):
    if (originalState[B_X_IND] == originalState[A_X_IND]):
        if (originalState[B_Y_IND] - originalState[A_Y_IND] == 1):
            x = 1
        elif (originalState[B_Y_IND] - originalState[A_Y_IND] == -1):
            x = 5
    elif (originalState[A_X_IND] - originalState[B_X_IND] == 1):
        if (originalState[B_Y_IND] == originalState[A_Y_IND]):
            x = 3
        elif (originalState[B_Y_IND] - originalState[A_Y_IND] == 1):
            x = 2
        elif (originalState[B_Y_IND] - originalState[A_Y_IND] == -1):
            x = 4

    if (BALL_AT_B == originalState[HAS_BALL_INDEX]):
        if (originalState[B_Y_IND] - GATEA_POS[0][0] == 0 or originalState[B_Y_IND] - GATEA_POS[1][0] == 0):
            y = 2
        elif (originalState[B_Y_IND] - GATEA_POS[0][0] < 0 or originalState[B_Y_IND] - GATEA_POS[1][0] < 0):
            y = 1
        else:
            y = 3
    else:
        if (originalState[B_Y_IND] - originalState[A_Y_IND] == 0):
            if (originalState[B_X_IND] - originalState[A_X_IND] < 0):
                y = 2
            else:
                y = -2
        elif (originalState[B_Y_IND] - originalState[A_Y_IND] < 0):
            if (originalState[B_X_IND] - originalState[A_X_IND] < 0):
                y = 1
            else:
                y = -1
        else:
            if (originalState[B_X_IND] - originalState[A_X_IND] < 0):
                y = 3
            else:
                y = -3


    return [x,y,originalState[HAS_BALL_INDEX]]

    # if (BALL_AT_B == originalState[HAS_BALL_INDEX]):
    #     distanceXToGate = originalState[B_X_IND] - GATEA_POS[0][1]
    #     distanceYToGate = originalState[B_Y_IND] - GATEA_POS[0][0]
    #     return [distanceXToGate, distanceYToGate, originalState[HAS_BALL_INDEX]]
    # else:
    #     distanceXToOpponent = originalState[A_X_IND] - originalState[B_X_IND]
    #     distanceYToOpponent = originalState[A_Y_IND] - originalState[B_Y_IND]
    #     return [distanceXToOpponent, distanceYToOpponent, originalState[HAS_BALL_INDEX]]
