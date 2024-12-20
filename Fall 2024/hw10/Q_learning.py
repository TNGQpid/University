import gymnasium as gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict

# Model: Chat-GPT 4-o, Prompt: Implement Q-Learning for CliffWalking-v0 based on the provided starter code,
# while using numpy's argmax function to select the action, and numpy's max function to calculate the expected reward.
# (+ excerpt from the starter code)

EPISODES =  30000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":
    env_name = "CliffWalking-v0"
    env = gym.envs.make(env_name)
    env.reset(seed=1)

    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()[0]

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done):

            if random.uniform(0,1) < EPSILON:
                action = env.action_space.sample()
            else:
                prediction = []
                for a in range(env.action_space.n):
                    prediction.append(Q_table[(obs,a)])
                prediction = np.array(prediction)
                action = np.argmax(prediction)
                    
            next_obs,reward,terminated,truncated,info = env.step(action)
            episode_reward += reward

            done = terminated or truncated

            if done:
                Q_table[(obs, action)] = Q_table[(obs, action)] + LEARNING_RATE * (reward - Q_table[(obs,action)])
            else:
                predictio = []
                for a in range(env.action_space.n):
                    predictio.append(Q_table[(next_obs,a)])
                predictio = np.array(predictio)
                expected_reward = np.max(predictio)
                Q_table[(obs, action)] = Q_table[(obs, action)] + \
                    LEARNING_RATE * (reward - Q_table[(obs, action)] + DISCOUNT_FACTOR * expected_reward)
                
            obs = next_obs
        EPSILON = EPSILON * EPSILON_DECAY
        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 
     
        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open(f'Q_TABLE_QLearning.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################