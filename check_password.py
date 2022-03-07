import numpy as np
import math

USER_FILE = "user"

P_HACKER = 0.9

def check(times):
    times.insert(0,1)
    t = np.array(times)
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip("\n")
    weights1 = f.readline().strip().split(",")
    weights2 = f.readline().strip().split(",")
    f.close()
    L = 2*len(password)-2
    w = []
    for i in range(len(weights1)):
        weights1[i] = float(weights1[i])
    for i in range(len(weights2)):
        weights2[i] = float(weights2[i])
    w.append(np.array(weights1).reshape(L, L+1))
    w.append(np.array(weights2))
    z0 = np.matmul(w[0], t)
    a0 = np.zeros(L+1)
    a0[0] = 1
    for i in range(1,L+1):
        a0[i] = sig(z0[i-1])
    z1 = np.matmul(w[1], a0)
    a1 = sig(z1)
    return a1

def get_password():
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip()
    f.close()
    return password

def sig(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1 / (1 + math.exp(-x))