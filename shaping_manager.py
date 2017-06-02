
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

        # *** Your code end *********** #

        return shaping_reward
