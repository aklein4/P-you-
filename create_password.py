from aiohttp import TraceRequestChunkSentParams
import numpy
import os
import numpy as np
import math
import random
import sys


DATA_FOLDERS = ["data/fixed_data", "data/free_data"]

USER_FILE = "user"
STEP = 1
THRESH = .001
TIMEOUT = 1000
P_HACKER = 0.4
N_MID = 0
TRACKING = True

def create(password, times):

    combos = get_combos(password)
    data = get_data(combos, password)

    for set in times:
        data.append([1]+set)

    weights = get_weights(data)
    f = open(USER_FILE+".txt", "w")
    f.write(password+"\n")
    line = ""
    for row in weights[0]:
        for x in row:
            line += ","+str(x)
    line += "\n"
    f.write(line[1:])
    line = ""
    for x in weights[1]:
        line += ","+str(x)
    line += "\n"
    f.write(line[1:])
    f.close()

    # save times:
    # f = open(USER_FILE+".txt", "w")
    # f.write(password+"\n")
    # for set in times:
    #     line = ""
    #     for t in set:
    #         line += ","+str(round(t))
    #     line += "\n"
    #     f.write(line[1:])
    # f.close()

def get_data(combos, password):
    data = []
    pass_list = []
    for i in range(len(password)-1):
        pass_list.append(password[i])
    for folder in DATA_FOLDERS:
        for file in os.listdir(folder):
            user = {}
            user_hold = {}
            num = 0
            total = 0
            total_hold = 0
            for com in combos:
                user[com] = []
            for ke in pass_list:
                user_hold[ke] = []
            user_file = open(folder+"/"+file, "r", encoding="utf-8")
            for line in user_file:
                num += 1
                clean = line.strip("\n").split(",")
                total += int(clean[2])
                total_hold += int(clean[3])
                if (clean[0], clean[1]) in combos:
                    user[(clean[0], clean[1])].append(int(clean[2]))
                if clean[1] in pass_list:
                    user_hold[clean[1]].append(int(clean[3]))
            user_file.close()
            if num != 0:
                avreg = total/num
                avreg_hold = total_hold/num
                for com in user.keys():
                    if user[com] == []:
                        user[com] = round(avreg)
                    else:
                        user[com] = round(sum(user[com])/len(user[com]))
                for ke in user_hold.keys():
                    if user_hold[ke] == []:
                        user_hold[ke] = round(avreg_hold)
                    else:
                        user_hold[ke] = round(sum(user_hold[ke])/len(user_hold[ke]))
                data.append([user, user_hold])
    clean_data = []
    for user in data:
        clean_user = [0]
        for com in combos:
            clean_user.append(user[0][com])
        for ke in pass_list:
            clean_user.append(user[1][ke])
        clean_data.append(clean_user)
    return clean_data

def get_hold_data(password):
    pass_list = []
    for i in range(len(password)-1):
        pass_list.append(password[i])
    data = []
    for folder in DATA_FOLDERS:
        for file in os.listdir(folder):
            user = {}
            num = 0
            total = 0
            for com in pass_list:
                user[com] = []
            user_file = open(folder+"/"+file, "r", encoding="utf-8")
            for line in user_file:
                num += 1
                clean = line.strip("\n").split(",")
                total += int(clean[3])
                if clean[1] in pass_list:
                    user[clean[1]].append(int(clean[3]))
            user_file.close()
            if num != 0:
                avreg = total/num
                for ke in user.keys():
                    if user[ke] == []:
                        user[ke] = round(avreg)
                    else:
                        user[ke] = round(sum(user[ke])/len(user[ke]))
                data.append(user)
    clean_data = []
    for user in data:
        clean_user = [0]
        for ke in pass_list:
            clean_user.append(user[ke])
        clean_data.append(clean_user)
    return clean_data

def get_combos(password):
    combos = []
    for i in range(1, len(password)):
        combos.append((password[i-1], password[i]))
    return combos

def get_weights(data, track=True):

    # prepare data
    L = len(data[0])-1
    for i in range(len(data)):
        data[i].insert(1,1)
    n_hack = 0
    n_user = 0
    for user in data:
        if user[0] == 1:
            n_user += 1
        else:
            n_hack += 1

    # Get initial weights
    theta_old = []
    # first layer 0
    theta_old.append(np.zeros((L,L+1)))
    for i in range(0,L):
        # 1 weight is on (-1,1)
        theta_old[0][i,0] = (random.random()*2)-1
        # weight for others is in {-4/500n, 4/500n}
        for j in range(1,L+1):
            theta_old[0][i,j] = random.choice([-1,1])*4/(500*L)
    # inter layers
    for layz in range(N_MID):
        theta_old.append(np.zeros((L,L+1)))
        for i in range(0,L):
            # 1 weight is on (-1,1)
            theta_old[0][i,0] = (random.random()*2)-1
            # weight for others is in {-4/500n, 4/500n}
            for j in range(1,L+1):
                theta_old[0][i,j] = random.choice([-1,1])*8/L
    # final layer
    theta_old.append(np.zeros(L+1))
    theta_old[1][0] = (random.random()*2)-1
    for i in range(1,L+1):
        theta_old[1][i] = random.choice([-1,1])*8/L

    err = THRESH*2
    n = 0
    err0 = -1
    while err > THRESH and n < TIMEOUT:
        if TRACKING:
            progress(2**abs(err-err0), 2**abs(err0-THRESH), suff=str(n)+": "+str(err))
        n += 1
        err = 0
        theta_new = []
        for layz in range(len(theta_old)):
            theta_new.append(theta_old[layz].copy())

        for pair in data:
            # inputs
            y = pair[0]
            x = np.array(pair[1:])
            a = []
            z = [numpy.matmul(theta_old[0], x)]
            grad = []
            for g in range(len(theta_old)):
                grad.append(0)
            for layz in range(N_MID+1):
                a.append(np.zeros(L+1))
                a[layz][0] = 1
                for i in range(1,L+1):
                    a[layz][i] = sig(z[layz][i-1])
                # input to next
                z.append(numpy.matmul(theta_old[layz+1], a[layz]))

            # output of final
            a_fin = sig(z[N_MID+1])

            # derivitive of error
            err_d = (y-a_fin)**2
            # err_d = abs(y-a1)
            # if err_d > 0.5:
            if y == 1:
                err_d *= (1-P_HACKER)/n_user
            else:
                err_d *= P_HACKER/n_hack
            err += err_d
            dE_dafin = -(y-a_fin)

            # change of output per final input
            dafin_dzfin = dsig(z[N_MID+1])
            # how much the final input should change
            delta_fin = dE_dafin*dafin_dzfin*STEP
            if y == 1:
                delta_fin *= (1-P_HACKER)/n_user
            else:
                delta_fin *= P_HACKER/n_hack
            # how the final input weights should change
            grad[N_MID+1] = delta_fin*a[N_MID]/np.linalg.norm(a[N_MID])

            delta_curr = delta_fin
            for layz in range(N_MID, -1, -1):
                # change in final input  from first output
                dzup_dame = theta_old[layz+1][1:]
                # change in first output from first input
                dame_dzme = np.zeros(L)
                for i in range(L):
                    dame_dzme[i] = dsig(z[layz][i])
                # how much each node input needs to change
                delta_curr = delta_curr*np.multiply(dame_dzme, np.transpose(dzup_dame))
                # how much first inputs need to change
                grad[layz] = np.tensordot(delta_curr, z[layz], axes=0)/np.linalg.norm(z[layz])

            for layz in range(len(grad)):
                theta_new[layz] += grad[layz]

        for layz in range(len(theta_old)):
                theta_new[layz] = theta_new[layz].copy()
        if err0==-1:
            err0 = err

    if TRACKING:
        progress(10, 10, done=True, suff=str(err))
    if n == TIMEOUT:
        print("Timed out.")
    return theta_old

def sig(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1 / (1 + math.exp(-x))

def dsig(x):
    return sig(x)*(1-sig(x))

def progress(count, total, bar_len=25, done=False, suff=""):
    suff = str(suff)
    # https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    perc = count/total
    if perc > 1:
        perc = 1
    if perc < 0:
        perc = 0
    bar = "\u25A0" * round(perc*bar_len)
    bar += "\u25A1" * round((1-perc)*bar_len)
    if not done:
        print(bar, suff, end="\r")
        return
    print(bar)

# L = 3-1
# pair = [1,1,200,300]
# # Get initial weights
# theta_old = []
# # layer 0
# theta_old.append(np.zeros((L,L+1)))
# for i in range(0,L):
#     # 1 weight is on (-1,1)
#     theta_old[0][i,0] = (random.random()*2)-1
#     # weight for others is in {-4/500n, 4/500n}
#     for j in range(1,L+1):
#         theta_old[0][i,j] = random.choice([-1,1])*4/(500*L)
# # layer 2
# theta_old.append(np.zeros(L+1))
# theta_old[1][0] = (random.random()*2)-1
# for i in range(1,L+1):
#     theta_old[1][i] = random.choice([-1,1])*8/L

# y = pair[0]
# x = np.array(pair[1:])
# z0 = numpy.matmul(theta_old[0], x)

# a0 = np.zeros(L+1)
# a0[0] = 1
# for i in range(1,L+1):
#     a0[i] = sig(z0[i-1])
# z1 = numpy.matmul(theta_old[1], a0)
# # output of final
# a1 = sig(z1)
# # derivitive of error
# dE_da1 = -(y-a1)
# # change of output per final input
# da1_dz1 = dsig(z1)
# # how much the final input should change
# delta1 = dE_da1*da1_dz1*STEP
# if y == 1:
#     delta1 /= 10
# else:
#     delta1 *= P_HACKER/100
# # how the final input weights should change
# grad1 = delta1*a0

# # change in final input  from first output
# dz1_da0 = theta_old[1][1:]
# # change in first output from first input
# da0_dz0 = np.zeros(L)
# for i in range(L):
#     da0_dz0[i] = dsig(z0[i])
# # how much each node input needs to change
# delta0 = delta1*np.multiply(da0_dz0, np.transpose(dz1_da0))
# print(delta0)
# # how much first inputs need to change
# grad0 = np.tensordot(delta0, x, axes=0)
# print(grad0)




# theta_old = [np.array([[1,2],[3,4]]), np.array([5,6])]
# L = 2
# y = 1
# x = np.array([1,2])
# z0 = numpy.matmul(theta_old[0], x)
# a0 = np.zeros(L)
# for i in range(L):
#     a0[i] = sig(z0[i])
# z1 = numpy.matmul(theta_old[1], a0)
# a1 = sig(z1)
# dE_da1 = -(y-a1)
# da1_dz1 = dsig(z1)
# delta1 = dE_da1*da1_dz1
# grad1 = delta1*a0

# dz1_da0 = theta_old[1]
# da0_dz0 = np.zeros(L)
# for i in range(L):
#     da0_dz0[i] = dsig(z0[i])
# delta0 = delta1*np.multiply(da0_dz0, np.transpose(dz1_da0))
# grad0 = np.tensordot(delta0, x, axes=0)

# if y == 1:
#     d1 /= n_user
# else:
#     d1 *= P_HACKER/n_hack
# d0 = np.multiply(dsig0, theta_old[0])*d1