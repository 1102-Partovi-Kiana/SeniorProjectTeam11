import gym
env = gym.make("FetchReach-v1")
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample())