from aiohttp import TraceRequestChunkSentParams
import numpy
import os
import numpy as np
import math
import sys

from sklearn.manifold import trustworthiness


DATA_FOLDERS = ["data/fixed_data", "data/free_data"]

USER_FILE = "user"
STEP = 1/10
THRESH = STEP/1000
TIMEOUT = 150
P_HACKER = 0.4

def create(password, times):

    combos = get_combos(password)
    data = get_data(combos)
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

def get_data(combos):
    data = []
    for folder in DATA_FOLDERS:
        for file in os.listdir(folder):
            user = {}
            num = 0
            total = 0
            for com in combos:
                user[com] = []
            user_file = open(folder+"/"+file, "r", encoding="utf-8")
            for line in user_file:
                num += 1
                clean = line.strip("\n").split(",")
                total += int(clean[2])
                if (clean[0], clean[1]) in combos:
                    user[(clean[0], clean[1])].append(int(clean[2]))
            user_file.close()
            if num != 0:
                avreg = total/num
                for com in user.keys():
                    if user[com] == []:
                        user[com] = round(avreg)
                    else:
                        user[com] = round(sum(user[com])/len(user[com]))
                data.append(user)
    clean_data = []
    for user in data:
        clean_user = [0]
        for com in combos:
            clean_user.append(user[com])
        clean_data.append(clean_user)
    return clean_data

def get_combos(password):
    combos = []
    for i in range(1, len(password)):
        combos.append((password[i-1], password[i]))
    return combos

def get_weights(data, track=True):
    L = len(data[0])
    for i in range(len(data)):
        data[i].append(1)
    n_hack = 0
    n_user = 0
    for user in data:
        if user[0] == 1:
            n_user += 1
        else:
            n_hack += 1
    theta_old = []
    theta_old.append(np.random.rand(L,L)/100)
    theta_old.append(np.random.rand(L)/100)
    dist = THRESH*2
    dist0 = THRESH*2
    t = 0
    tot = 0
    while dist > THRESH or t < TIMEOUT:
        tot = 0
        if track:
            progress(t, TIMEOUT, suff="dist: "+str(dist))
        theta_new = theta_old.copy()
        for pair in data:
            y = pair[0]
            x = np.transpose(np.array(pair[1:]))
            z0 = numpy.matmul(theta_old[0], x)
            a0 = np.zeros(L)
            for i in range(L):
                a0[i] = sig(z0[i])
            z1 = numpy.matmul(theta_old[1], a0)
            a1 = sig(z1)
            dE_da1 = -(y-a1)
            da1_dz1 = dsig(z1)
            delta1 = dE_da1*da1_dz1*STEP
            if y == 1:
                delta1 /= n_user
            else:
                delta1 *= P_HACKER/n_hack
            grad1 = delta1*a0

            dz1_da0 = theta_old[1]
            da0_dz0 = np.zeros(L)
            for i in range(L):
                da0_dz0[i] = dsig(z0[i])
            delta0 = delta1*np.multiply(da0_dz0, np.transpose(dz1_da0))
            grad0 = np.tensordot(delta0, x, axes=0)

            theta_new[0] -= grad0
            theta_new[1] -= grad1
        dist = np.linalg.norm(1)
        print(tot)
        if dist0 == THRESH*2:
            dist0 = dist
        theta_old = theta_new.copy()
        t += 1
    if track:
        progress(10, 10, done=True, suff="dist: "+str(dist))
    print(t)
    return theta_old

def sig(x):
    if x < -20:
        return 0
    if x > 20:
        return 1
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