def has_ball(state, player):
    """
    Tell if the given player has the ball in the given state
    :param state: the state
    :param player: "A" for A, anything else for B
    :return: True or False
    """
    a_has_the_ball = state[4]
    return bool(a_has_the_ball ^ (player == "A"))


def manhattan_dist_between_players(state):
    return abs(state[0]-state[2]) + abs(state[1]-state[3])


def manhattan_dist_from_left_gate(state):
    return state[0]+state[1], state[2]+state[3]


class ShapingManager:

    def __init__(self):
        # *** You can add and initiate private members here *** #
        pass
        # ************** #

    def get_shaping_reward(self, previous_state, action, current_state):
        """
        The function should return the shaping reward for the learning agent.
        States structure is:
            [0] player A's x coordinate
            [1] player A's y coordinate
            [2] player B's x coordinate
            [3] player B's y coordinate
            [4] ball status: 0= B has the ball, 1= A has the ball
        :param previous_state: integer[5], see description for details. source state- s.
        :param action: integer. the action that performed by b. possible values:
            0=  up
            1=  down
            2=  left
            3=  right
            4=  stay in place
        :param current_state: integer[5], see description for details. target state- s'.
        :return: the value of F(s, a, s')
        """
        shaping_reward = 0

        # *** Your code begins here *** #
        if has_ball(previous_state, "B") and has_ball(current_state, "A"):
            return -0.025

        if has_ball(previous_state, "A") and has_ball(current_state, "B"):
            return 0.025

        prev_a_dist, prev_b_dist = manhattan_dist_from_left_gate(previous_state)
        curr_a_dist, curr_b_dist = manhattan_dist_from_left_gate(current_state)
        prev_dist = manhattan_dist_between_players(previous_state)
        curr_dist = manhattan_dist_between_players(current_state)
        if has_ball(current_state, "A"):
            # 1. A has the ball and is closer to left gate = almost certain loss
            if curr_a_dist < curr_b_dist:
                return -0.075
            # 2. A has the ball, but action gets B closer to A = good
            if curr_dist < prev_dist:
                return 0.05
        else:
            if curr_b_dist < curr_a_dist:
                return -0.05

        # *** Your code end *********** #

        return shaping_reward