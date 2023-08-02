import numpy as np
from ppo_torch import Agent
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import reward
import Functions as func

channel = EngineConfigurationChannel()
env = UnityEnvironment(file_name='CoE202', side_channels=[channel])
channel.set_configuration_parameters(time_scale=15)

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
                input_dims=obs_p1.shape, chkpt_dir = "p1_strk1")
agent_p2 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "p2_keep1")
agent_b1 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "b1_strk1")
agent_b2 = Agent(n_actions=15, batch_size=batch_size,
                alpha=alpha, n_epochs=n_epochs,
                input_dims=obs_p1.shape, chkpt_dir = "b2_keep1")


n_games = 100000
best_score_p1, best_score_p2, best_score_b1, best_score_b2 = -99999, -99999, -99999, -99999
score_history_p1, score_history_p2, score_history_b1, score_history_b2 = [], [], [], []
learn_iters = 0
avg_score_p1, avg_score_p2, avg_score_b1, avg_score_b2 = 0, 0, 0, 0
n_steps = 0

for i in range(n_games):
    env.reset()

    behavior_name_1 = list(env.behavior_specs)[0]
    behavior_name_2 = list(env.behavior_specs)[1]
    decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
    decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

    obs_p1, obs_p2, obs_b1, obs_b2 = func.get_state(decision_steps_p, decision_steps_b)

    observation_p1 = np.reshape(obs_p1, 112)
    observation_p2 = np.reshape(obs_p2, 112)
    observation_b1 = np.reshape(obs_b1, 112)
    observation_b2 = np.reshape(obs_b2, 112)

    done = False
    score_p1, score_p2, score_b1, score_b2 = 0, 0, 0, 0

    t = 0
    while not done:
        t+=1
        a_p1, prob_p1, val_p1 = agent_p1.choose_action(observation_p1)
        a_p2, prob_p2, val_p2 = agent_p2.choose_action(observation_p2)
        a_b1, prob_b1, val_b1 = agent_b1.choose_action(observation_b1)
        a_b2, prob_b2, val_b2 = agent_b2.choose_action(observation_b2)

        action_p1 = action_list[a_p1]
        action_p2 = action_list[a_p2]
        action_b1 = action_list[a_b1]
        action_b2 = action_list[a_b2]

        co_p1, co_back_p1, co_p2, co_back_p2, co_b1, co_back_b1, co_b2, co_back_b2 = func.get_cur_obs(decision_steps_p,
                                                                                                      decision_steps_b)

        # action_p1, a_p1 = func.logic(co_p1, co_back_p1, action_p1, a_p1, avg_score_p1, "s", i)
        # action_p2, a_p2 = func.logic(co_p2, co_back_p2, action_p2, a_p2, avg_score_p2, "k", i)
        # action_b1, a_b1 = func.logic(co_b1, co_back_b1, action_b1, a_b1, avg_score_b1, "s", i)
        # action_b2, a_b2 = func.logic(co_b2, co_back_b2, action_b2, a_b2, avg_score_b2, "k", i)


        env.set_actions(behavior_name_1, np.array([action_p1, action_p2]))
        env.set_actions(behavior_name_2, np.array([action_b1, action_b2]))

        env.step()

        behavior_name_1 = list(env.behavior_specs)[0]
        behavior_name_2 = list(env.behavior_specs)[1]
        decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
        decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

        obs_p1_, obs_p2_, obs_b1_, obs_b2_ = func.get_state(decision_steps_p, decision_steps_b)

        observation_p1_ = np.reshape(obs_p1_, 112)
        observation_p2_ = np.reshape(obs_p2_, 112)
        observation_b1_ = np.reshape(obs_b1_, 112)
        observation_b2_ = np.reshape(obs_b2_, 112)

        co_p1, co_back_p1, co_p2, co_back_p2, co_b1, co_back_b1, co_b2, co_back_b2 = func.get_cur_obs(decision_steps_p, decision_steps_b)

        # r_p1 = reward.get_reward_1(co_p1, co_back_p1, decision_steps_p.reward[0])
        # r_p2 = reward.get_reward_1(co_p2, co_back_p2, decision_steps_p.reward[0])
        # r_b1 = reward.get_reward_1(co_b1, co_back_b1, decision_steps_b.reward[0])
        # r_b2 = reward.get_reward_1(co_b2, co_back_b2, decision_steps_b.reward[0])

        # r_p1 = reward.get_reward_2(co_p1, co_back_p1, decision_steps_p.reward[0])
        # r_p2 = reward.get_reward_2(co_p2, co_back_p2, decision_steps_p.reward[0])
        # r_b1 = reward.get_reward_2(co_b1, co_back_b1, decision_steps_b.reward[0])
        # r_b2 = reward.get_reward_2(co_b2, co_back_b2, decision_steps_b.reward[0])

        r_p1 = reward.get_reward_striker(co_p1, co_back_p1, decision_steps_p.reward[0])
        r_p2 = reward.get_reward_keeper(co_p2, co_back_p2, decision_steps_p.reward[0])
        r_b1 = reward.get_reward_striker(co_b1, co_back_b1, decision_steps_b.reward[0])
        r_b2 = reward.get_reward_keeper(co_b2, co_back_b2, decision_steps_b.reward[0])

        n_steps += 1

        score_p1 += r_p1
        score_p2 += r_p2
        score_b1 += r_b1
        score_b2 += r_b2

        if decision_steps_b.reward[0] != 0:
            env.reset()
            behavior_name_1 = list(env.behavior_specs)[0]
            behavior_name_2 = list(env.behavior_specs)[1]
            decision_steps_p, terminal_steps_p = env.get_steps(behavior_name_1)
            decision_steps_b, terminal_steps_b = env.get_steps(behavior_name_2)

            obs_p1, obs_p2, obs_b1, obs_b2 = func.get_state(decision_steps_p, decision_steps_b)

            observation_p1_ = np.reshape(obs_p1, 112)
            observation_p2_ = np.reshape(obs_p2, 112)
            observation_b1_ = np.reshape(obs_b1, 112)
            observation_b2_ = np.reshape(obs_b2, 112)

        if t == 255 or decision_steps_b.reward[0] != 0:
            done = True

        agent_p1.remember(observation_p1, a_p1, prob_p1, val_p1, r_p1, done)
        agent_p2.remember(observation_p2, a_p2, prob_p2, val_p2, r_p2, done)
        agent_b1.remember(observation_b1, a_b1, prob_b1, val_b1, r_b1, done)
        agent_b2.remember(observation_b2, a_b2, prob_b2, val_b2, r_b2, done)

        if n_steps % N == 0:
            agent_p1.learn()
            agent_p2.learn()
            agent_b1.learn()
            agent_b2.learn()
            learn_iters += 1

        observation_p1 = observation_p1_
        score_history_p1.append(score_p1)
        avg_score_p1 = np.mean(score_history_p1[-200:])

        observation_p2 = observation_p2_
        score_history_p2.append(score_p2)
        avg_score_p2 = np.mean(score_history_p2[-200:])

        observation_b1 = observation_b1_
        score_history_b1.append(score_b1)
        avg_score_b1 = np.mean(score_history_b1[-200:])

        observation_b2 = observation_b2_
        score_history_b2.append(score_b2)
        avg_score_b2 = np.mean(score_history_b2[-200:])

        if i > 0:
            if avg_score_p1 > best_score_p1:
                best_score_p1 = avg_score_p1
                agent_p1.save_models(i)

            if avg_score_p2 > best_score_p2:
                best_score_p2 = avg_score_p2
                agent_p2.save_models(i)

            if avg_score_b1 > best_score_b1:
                best_score_b1 = avg_score_b1
                agent_b1.save_models(i)

            if avg_score_b2 > best_score_b2:
                best_score_b2 = avg_score_b2
                agent_b2.save_models(i)

            if decision_steps_b.reward[0] != 0:
                if decision_steps_b.reward[0] > 0:
                    agent_b1.save_models(i)
                    agent_b2.save_models(i)
                else:
                    agent_p1.save_models(i)
                    agent_p2.save_models(i)

    print('episode', i, 'score_p1 %.1f' % score_p1, 'score_p2 %.1f' % score_p2, 'score_b1 %.1f' % score_b1,\
          'score_b2 %.1f' % score_b2, 'avg_score_p1 %.1f' % avg_score_p1, 'avg_score_p2 %.1f' % avg_score_p2,\
          'avg_score_b1 %.1f' % avg_score_b1, 'avg_score_b2 %.1f' % avg_score_b2 ,'time_steps', n_steps, 'learning_steps', learn_iters)