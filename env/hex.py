import gymnasium as gym

class HexEnv(gym.Env):

    metadata = {
        'render.modes': ['human', 'rgb_array'],
    }

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass