def get_reward_1(sig, sig_back, goal):
    if goal != 0:
        if goal > 0:
            return 50 * goal
        else:
            return -40

    # 앞에 우리 골대
    for i in range(7):
        if sig[i][1] == 1:
            return -15
    ## ## ##

    # 뒤에 상대 골대
    for i in range(3):
        if sig_back[i][2] == 1:
            return -15
    ## ## ##

    #뒤에 다 바로 벽
    if sig_back[0][3] == 1 and sig_back[1][3] == 1 and sig_back[2][3] == 1:
            if sig_back[0][7] < 0.1 and sig_back[1][7] < 0.1 and sig_back[2][7] < 0.1:
                return -2
    ## ## ##

    # 볼이 앞에 있을 시
    ball_s = -1
    ball_dis = -1

    for i in range(11):
        if sig[i][0] == 1:
            ball_s = i
            ball_dis = sig[ball_s][7]

    if ball_s != -1 and ball_dis < 0.3:
        if ball_s == 0:
            return 10
        elif ball_s < 5:
            return 5
        elif ball_s < 7:
            return 4
        else:
            return 1
    ## ## ##

    # 뒤에 볼 감지 시
    if sig_back[0][0] == 1:
        return -15

    for i in range(1,3):
        if sig_back[i][0] == 1:
            return -5
    ## ## ##

    return 0

def get_reward_2(obs, obs_back, goal):
    if goal != 0:
        if goal > 0:
            return 50 * goal
        else:
            return -40

    reward = 0
    b_ext = -1
    b_dis = 0
    gp_ext = 0
    gp_dis = 0

    for i in range(11):
        if obs[10-i][0]==1:
            b_dis = obs[10-i][7]
            if 10-i < 7:
                b_ext = 2
            elif 10-i > 6:
                b_ext = 1

    # for i in range(3):
    #     if obs_back[2-i][0] == 1:
    #         b_dis = obs[2-i][7]
    #         b_ext = -1

    for i in range(11):
        if obs[10-i][2] == 1:
            gp_dis = obs[10-i][7]
            if 10-i < 7:
                gp_ext = 1
            elif 10-i > 6:
                gp_ext = 0.8

    for i in range(3):
        if obs_back[2-i][2] == 1:
            gp_dis = obs[2-i][7]
            gp_ext = 0.1

    if b_ext > 0:
        reward = b_ext * (100**(1-b_dis)/10) + gp_ext * b_ext * (100**(1-b_dis)/10) * (30**(1-gp_dis)/10)
    else:
        reward = -4

    return reward


def get_reward_striker(signal, signal_back, goal):
    if goal > 0:
        return 50 * goal

    if goal < 0:
        return -20

    re = 0
    # 공이 시야에 있을때
    ball_insight = True if signal[0][0] == 1 or signal[1][0] == 1 or signal[2][0] == 1 or signal[3][0] == 1 or signal[4][0] == 1 or signal[5][0] == 1 or signal[6][0] == 1 else False
    if ball_insight:
        re += 0.05

    #서서히 공을 바라보도록
    if signal[0][0] == 1:
        re += 0.1
    if signal[1][0] == 1 or signal[2][0] == 1:
        re += 0.03
    if signal[3][0] == 1 or signal[4][0] == 1:
        re += 0.01
    if signal[5][0] == 1 or signal[6][0] == 1:
        re += 0.001

    # 공이 안보일 경우 적당히 뒤로 가도록
    if not ball_insight and signal_back[0][1] == 1:
        re += 0.1 * 1 / (signal_back[0][7] + 1) # 최대값 0.1

    # 공이 가까울수록, 하지만 더 공격적으로
    if signal[0][0] == 1:
        re += 2 * 1 / (signal[0][7] + 0.1) # 최대값 20

    return re

def get_reward_keeper(signal, signal_back, goal):
    if goal < 0:
        return -50

    if goal > 0:
        return 20

    re = 0
    #공이 시야에 있을때
    ball_insight = True if signal[0][0]==1 or signal[1][0]==1 or signal[2][0]==1 or signal[3][0]==1 or signal[4][0]==1 or signal[5][0]==1 or signal[6][0]==1 else False
    if ball_insight:
        re += 0.05

    #서서히 공을 바라보도록
    if signal[0][0] == 1:
        re += 0.1
    if signal[1][0] == 1 or signal[2][0] == 1:
        re += 0.03
    if signal[3][0] == 1 or signal[4][0] == 1:
        re += 0.01
    if signal[5][0] == 1 or signal[6][0] == 1:
        re += 0.001

    #공이 안보일 경우 많이 뒤로 가도록
    if not ball_insight and signal_back[0][1]==1:
        re += 0.1 * 1 / (signal_back[0][7] + 0.5) #최대값 0.2
    if not ball_insight and signal_back[1][1]==1 or not ball_insight and signal_back[1][1]==1:
        re += 0.05 * 1 / (signal_back[0][7] + 0.5) # 최대값 0.1

    #공이 가까울수록, 하지만 덜 공격적으로
    if signal[0][0]==1:
        re += 0.5 * 1 / (signal[0][7] + 0.1) #최대값 5

    #자책골 방지
    if signal_back[0][0]==1:
        re -= 0.1 * 1 / (signal_back[0][7] + 0.5) # 최대값 0.2

    return re