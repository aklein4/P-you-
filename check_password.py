import numpy as np
import math

USER_FILE = "user"

def check(times):
    times.insert(0,1)
    t = np.array(times)
    weights = []
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip("\n")
    for line in f:
        weights.append(line.strip().split(","))
    f.close()
    L = 2*len(password)-2
    w = []
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j] = float(weights[i][j])
    for layz in range(0,len(weights)-1):
        curr = np.array(weights[layz])
        w.append(curr.reshape(L, L+1))
    w.append(np.array(weights[-1]))
    a = []
    z = [np.matmul(w[0], t)]
    grad = []
    for layz in range(len(w)-1):
        a.append(np.zeros(L+1))
        a[layz][0] = 1
        for i in range(1,L+1):
            a[layz][i] = sig(z[layz][i-1])
        # input to next
        if(layz <= len(w)-1):
            z.append(np.matmul(w[layz+1], a[layz]))

    # output of final
    a_fin = sig(z[len(w)-1])

    return a_fin

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