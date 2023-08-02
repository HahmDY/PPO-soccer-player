import numpy as np
from ppo_torch_test import Agent
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import reward
import Functions as func

channel = EngineConfigurationChannel()
env = UnityEnvironment(file_name='CoE202', side_channels=[channel])
channel.set_configuration_parameters(time_scale=1)

action_list = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 2, 0], [0, 2, 1],
                       [0, 2, 2], [1, 0, 0], [1, 0, 1], [1, 0, 2], [2, 0, 0], [2, 0, 1], [2, 0, 2]]

env.reset()

behavior_name_1 = list(env.behavior_specs)[0]
behavior_name_2 = list(env.behavior_specs)[1]
decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

obs_p1, obs_p2, obs_b1, obs_b2 = func.get_state(decision_steps_p, decision_steps_b)

obs_p1 = np.reshape(obs_p1, 112)

N = 64
batch_size = 8
n_epochs = 8
alpha = 0.0003

agent_p1 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "p1_strk2")
agent_p2 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "p2_keep2")
agent_b1 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "b1_strk2")
agent_b2 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "b2_keep2")



agent_p1.load_models()
agent_p2.load_models()
agent_b1.load_models()
agent_b2.load_models()

env.reset()

p_score = 0
b_score = 0

for i in range(100000):

    behavior_name_1 = list(env.behavior_specs)[0]
    behavior_name_2 = list(env.behavior_specs)[1]
    decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
    decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

    obs_p1, obs_p2, obs_b1, obs_b2 = func.get_state(decision_steps_p, decision_steps_b)

    observation_p1 = np.reshape(obs_p1, 112)
    observation_p2 = np.reshape(obs_p2, 112)
    observation_b1 = np.reshape(obs_b1, 112)
    observation_b2 = np.reshape(obs_b2, 112)


    a_p1, prob_p1, val_p1 = agent_p1.choose_action(observation_p1)
    a_p2, prob_p2, val_p2 = agent_p2.choose_action(observation_p2)
    a_b1, prob_b1, val_b1 = agent_b1.choose_action(observation_b1)
    a_b2, prob_b2, val_b2 = agent_b2.choose_action(observation_b2)

    action_p1 = action_list[a_p1]
    action_p2 = action_list[a_p2]
    action_b1 = action_list[a_b1]
    action_b2 = action_list[a_b2]

    env.set_actions(behavior_name_1, np.array([action_p1, action_p2]))
    env.set_actions(behavior_name_2, np.array([action_b1, action_b2]))

    env.step()

    if decision_steps_b.reward[0] != 0:
        env.reset()
        if decision_steps_b.reward[0] > 0:
            b_score += 1
        else:
            p_score += 1
        print("  Purple : Blue  |  " + str(p_score) + " : " + str(b_score))