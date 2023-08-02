def logic(sig, sig_back):
    ball_s = -1
    for i in range(11):
        if sig[i][0] == 1:
            ball_s = i
            ball_dis = sig[ball_s][7]

    ######## 바로 앞에 우리 골대 ###########
    if sig[0][1] == 1:
        if sig[0][1] < 0.12:
            return [1,0,0]

    #######앞에 우리 골대##########
    ourgp_dis_f = 0
    for i in range(7):
        if sig[i][1] == 1:
            ourgp_dis = sig[i][7]
            # 방향 잘 추가하기
            if ourgp_dis > 0.1:
                return [0, 0, 1]
            #action[2] = 2

    #######뒤에 상대 골대##########
    oppgp_dis_b = 0
    for i in range(3):
        if sig_back[i][2] == 1:
            oppgp_dis_b = sig_back[i][7]
            # action[2] = 2
            return [1, 0, 1]

    ####### 바로 뒤에 다 벽 ##########
    if sig_back[0][3] == 1 and sig_back[1][3] == 1 and sig_back[2][3] == 1:
        if sig_back[0][7] < 0.1 and sig_back[1][7] < 0.1 and sig_back[2][7] < 0.1:
            return [1,0,1]

    action = [-1, -1, -1]

    ball_s = -1
    ball_dis = -1
    ball_back_s = -1

    ######## 앞에 공 ########
    for i in range(11):
        if sig[i][0] == 1:
            ball_s = i
            ball_dis = sig[ball_s][7]

    #볼방향으로 회전
    if ball_s % 2 == 0:
        action[2] = 1
    elif ball_s % 2 == 1:
        action[2] = 2
    if ball_s == 0:
        action[2] = 0

    #앞에 있으면 전진
    if ball_s != -1:
        action[0] = 1

    if ball_s > 4:
        action[0] = 2

    if ball_s == -1:
        action[0] = 2

    ####바로 뒤에 우리 골대 있을 때 #####
    ourgp_dis_b = 10
    for i in range(3):
        if sig_back[i][1] == 1:
            ourgp_dis_b = min(ourgp_dis_b, sig_back[i][7])
        if ourgp_dis_b < 0.15 and ball_dis < 0.4:
            action[0] = 0
        if ourgp_dis_b < 0.15 and ball_dis < 0.1:
            action[0] = 1

    ######## 뒤 #########
    for i in range(3):
        if sig_back[i][0] == 1:
            ball_back_s = i

    #뒤에 공 감지 시 후진
    if ball_back_s == 1 or ball_back_s == 2:
        return [2, 0, 0]
        #방향 나중에 추가하기
    if ball_back_s == 0:
        return [2, 0, 1]
        #action[2] = 2

    #상대 골대 근점했을 때
    #우리 골대 너무 가까우면
    if action[0] == -1:
        action[0] = 0
    if action[1] == -1:
        action[1] = 0
    if action[2] == -1:
        action[2] = 0

    return action

def use_logic(sig, sig_back):
    ball_s = -1
    ball_dis = -1
    ball_back_s = -1


    for i in range(11):
        if sig[i][0] == 1:
            ball_s = i
            ball_dis = sig[ball_s][7]

    #가까운 거리 앞에 공 있을 시
    if ball_s != -1 and ball_dis < 0.3:
        return True

    #바로 뒤에 다 벽
    if sig_back[0][3] == 1 and sig_back[1][3] == 1 and sig_back[2][3] == 1:
        if sig_back[0][7] < 0.1 and sig_back[1][7] < 0.1 and sig_back[2][7] < 0.1:
            return True

    #바로 앞에 우리 골대 있을 시
    if sig[0][1] == 1 and sig[1][1] == 1 and sig[2][1] == 1:
        if sig[0][1] < 0.15 and sig[1][1] < 0.15 and sig[2][1] < 0.15:
            return True

    #뒤에 볼 감지 시
    if sig_back[0][0] == 1 or sig_back[1][0] == 1 or sig_back[2][0] == 1:
            return True

    #앞에 우리 골대
    for i in range(7):
        if sig[i][1] == 1 and sig[i][7] > 0.15:
            return True

    #뒤에 상대 골대
    for i in range(3):
        if sig_back[i][2] == 1:
            return True

    return False