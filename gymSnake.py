import gymnasium as gym
import numpy as np
import random

from gymnasium.envs.registration import register

register(
    id='snake-v0',
    entry_point='project:SnakeEnv',
)

#a lot of this is taken from HW2
# Main Function that does the reinforcement learning
env = gym.make('snake-v0', render_mode = 'human')
n_states = env.observation_space.n
n_actions = env.action_space.n
scores = np.zeros((n_states, n_actions))

alpha = 0.1      # Learning rate
gamma = 0.95      # Discount factor
epsilon = 1.0    # Exploration rate
epsilon_decay = 0.9995
epsilon_min = 0.1
episodes = 2000
max_steps = 1000

# Step 3: Training loop
for episode in range(episodes):
    # TODO: Reset environment and initialize variables
    state, info = env.reset()
    total_reward = 0

    for step in range(max_steps):
        # TODO: Choose an action (explore or exploit)
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() #Explore
        else:
            action = np.argmax(scores[state]) #Exploit

        # TODO: Take the action
        next_state, reward, done, truncated, info = env.step(action)

        # TODO: Update Q-table
        best_next = np.argmax(scores[next_state])
        scores[state, action] += alpha * (reward + gamma * (scores[next_state, best_next] - scores[state, action]))

        # TODO: Update state and reward tracker
        state = next_state
        total_reward += reward

        if done or truncated:
            break

    # TODO: Decay epsilon
    epsilon = max(epsilon_min, epsilon_decay * epsilon)

    if (episode + 1) % 200 == 0:
        print(f"Episode {episode+1}/{episodes} complete")

print("\nTraining complete!")

# Step 4: Test the trained agent
state, info = env.reset()
done = False
total_test_reward = 0

print("\n--- TESTING TRAINED AGENT ---")
for step in range(max_steps):
    # TODO: Always pick the best action
    action = np.argmax(scores[state])

    next_state, reward, done, truncated, info = env.step(action)
    total_test_reward += reward
    print(env.render())
    print("Total Reward:", total_test_reward)

    if done or truncated:
        break
    state = next_state

print("Total reward after training:", total_test_reward)
env.close()

