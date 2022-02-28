import numpy as np
import math

USER_FILE = "user"

P_HACKER = 0.4

def check(times):
    times.append(1)
    t = np.array(times)
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip("\n")
    weights = f.readline().strip().split(",")
    f.close()
    for i in range(len(weights)):
        weights[i] = float(weights[i])
    theta = np.array(weights)
    return sigmoid(np.dot(theta, t))

def get_password():
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip()
    f.close()
    return password

def sigmoid(x):
    if x < -20:
        return 0
    if x > 20:
        return 1
    return 1 / (1 + math.exp(-x))