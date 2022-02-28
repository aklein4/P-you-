import numpy
import os
import numpy as np
import math

DATA_FOLDERS = ["data/fixed_data", "data/free_data"]

USER_FILE = "user"
STEP = 0.0001
THRESH = STEP/10
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
    for w in weights:
        line += ","+str(w)
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

def get_weights(data):
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
    theta_old = np.full(L, .01)
    dist = THRESH*2
    while dist > THRESH:
        theta_new = theta_old.copy()
        for i in range(len(data)):
            y = data[i][0]
            x = np.array(data[i][1:])
            delta = STEP*(y-sigmoid(np.dot(theta_old, x)))*x
            if y == 1:
                delta /= n_user
            else:
                delta *= P_HACKER/n_hack
            theta_new += delta
        dist = np.linalg.norm(theta_new-theta_old)
        theta_old = theta_new.copy()
    return theta_old

def sigmoid(x):
    x = x/10
    if x < -20:
        return 0
    if x > 20:
        return 1
    return 1 / (1 + math.exp(-x))