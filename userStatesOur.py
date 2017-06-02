from constans import *
import copy

# state[0] = A_X_IND
# state[1] = A_Y_IND
# state[2] = B_X_IND
# state[3] = B_Y_IND
# state[4] = HAS_BALL_INDEX

# BALL_AT_A = 1
# BALL_AT_B = 0

def getUserState(originalState, action):

    if (BALL_AT_B == originalState[HAS_BALL_INDEX]):
        distanceXToGate = originalState[B_X_IND] - GATEA_POS[0][1]
        distanceYToGate = originalState[B_Y_IND] - GATEA_POS[0][0]
        return [distanceXToGate, distanceYToGate, originalState[HAS_BALL_INDEX]]
    else:
        distanceXToOpponent = originalState[A_X_IND] - originalState[B_X_IND]
        distanceYToOpponent = originalState[A_Y_IND] - originalState[B_Y_IND]
        return [distanceXToOpponent, distanceYToOpponent, originalState[HAS_BALL_INDEX]]

    # return [originalState[B_X_IND],originalState[B_Y_IND],originalState[A_X_IND],originalState[A_Y_IND]]