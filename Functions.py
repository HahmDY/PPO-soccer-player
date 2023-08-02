import numpy as np

def sensor_front_sig(data):
    player = []
    sensor_data = []
    for sensor in range(33):
        player.append(data[8 * sensor:(8 * sensor) + 8])

    for stack in range(3):
        sensor_data.append(player[11 * stack:(11 * stack) + 11])

    return sensor_data


def sensor_back_sig(data):
    player = []
    sensor_data = []
    for sensor in range(9):
        player.append(data[8 * sensor:(8 * sensor) + 8])

    for stack in range(3):
        sensor_data.append(player[3 * stack:(3 * stack) + 3])

    return sensor_data

def get_state(decision_steps_p, decision_steps_b):
    signal_p1 = sensor_front_sig(decision_steps_p.obs[0][0, :])[2]
    signal_back_p1 = sensor_back_sig(decision_steps_p.obs[1][0, :])[2]
    signal_p2 = sensor_front_sig(decision_steps_p.obs[0][1, :])[2]
    signal_back_p2 = sensor_back_sig(decision_steps_p.obs[1][1, :])[2]
    signal_b1 = sensor_front_sig(decision_steps_b.obs[0][0, :])[2]
    signal_back_b1 = sensor_back_sig(decision_steps_b.obs[1][0, :])[2]
    signal_b2 = sensor_front_sig(decision_steps_b.obs[0][1, :])[2]
    signal_back_b2 = sensor_back_sig(decision_steps_b.obs[1][1, :])[2]

    signal_p1 = np.reshape(signal_p1, [1, 88])
    signal_p2 = np.reshape(signal_p2, [1, 88])
    signal_b1 = np.reshape(signal_b1, [1, 88])
    signal_b2 = np.reshape(signal_b2, [1, 88])
    signal_back_p1 = np.reshape(signal_back_p1, [1, 24])
    signal_back_p2 = np.reshape(signal_back_p2, [1, 24])
    signal_back_b1 = np.reshape(signal_back_b1, [1, 24])
    signal_back_b2 = np.reshape(signal_back_b2, [1, 24])

    state_p1 = np.concatenate((signal_p1[0], signal_back_p1[0]), axis=0)
    state_p2 = np.concatenate((signal_p2[0], signal_back_p2[0]), axis=0)
    state_b1 = np.concatenate((signal_b1[0], signal_back_b1[0]), axis=0)
    state_b2 = np.concatenate((signal_b2[0], signal_back_b2[0]), axis=0)
    state_p1 = np.reshape(state_p1, [1, 112])
    state_p2 = np.reshape(state_p2, [1, 112])
    state_b1 = np.reshape(state_b1, [1, 112])
    state_b2 = np.reshape(state_b2, [1, 112])

    return state_p1, state_p2, state_b1, state_b2

def get_cur_obs(decision_steps_p, decision_steps_b):
    signal_p1 = sensor_front_sig(decision_steps_p.obs[0][0, :])
    signal_back_p1 = sensor_back_sig(decision_steps_p.obs[1][0, :])
    signal_p2 = sensor_front_sig(decision_steps_p.obs[0][1, :])
    signal_back_p2 = sensor_back_sig(decision_steps_p.obs[1][1, :])
    signal_b1 = sensor_front_sig(decision_steps_b.obs[0][0, :])
    signal_back_b1 = sensor_back_sig(decision_steps_b.obs[1][0, :])
    signal_b2 = sensor_front_sig(decision_steps_b.obs[0][1, :])
    signal_back_b2 = sensor_back_sig(decision_steps_b.obs[1][1, :])

    obs_p1 = signal_p1[2]
    obs_back_p1 = signal_back_p1[2]
    obs_p2 = signal_p2[2]
    obs_back_p2 = signal_back_p2[2]
    obs_b1 = signal_b1[2]
    obs_back_b1 = signal_back_b1[2]
    obs_b2 = signal_b2[2]
    obs_back_b2 = signal_back_b2[2]

    return obs_p1, obs_back_p1, obs_p2, obs_back_p2, obs_b1, obs_back_b1, obs_b2, obs_back_b2