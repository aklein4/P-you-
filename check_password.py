import numpy as np
import math
import scipy.stats

USER_FILE = "user"
P_HACKER = 0.4

def check(times):
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip("\n")
    me_vals = f.readline().strip().split(",")
    not_vals = f.readline().strip().split(",")

    me_mean = float(me_vals[0])
    me_std = float(me_vals[1])

    not_mean = float(not_vals[0])
    not_std = float(not_vals[1])

    divv = sum(times[0:len(password)])
    for i in range(len(times)):
            times[i] / divv

    times.insert(0,1)
    t = np.array(times)
    weights = []
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
    for layz in range(len(w)-1):
        a.append(np.zeros(L+1))
        a[layz][0] = 1
        for i in range(1,L+1):
            a[layz][i] = sig(z[layz][i-1])
        # input to next
        if(layz <= len(w)-1):
            z.append(np.matmul(w[layz+1], a[layz]))

    # output of final
    a_fin = math.log10(sig(z[len(w)-1]))

    prob = scipy.stats.norm.pdf(a_fin,loc=me_mean,scale=me_std)*(1-P_HACKER)/(
                scipy.stats.norm.pdf(a_fin,loc=not_mean,scale=not_std)*P_HACKER+scipy.stats.norm.pdf(a_fin,loc=me_mean,scale=me_std)*(1-P_HACKER)
                )

    return prob

def get_password():
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip()
    f.close()
    return password

def feed(password, weights, t):
    L = 2*len(password)-2
    w = []
    for layz in range(0,len(weights)-1):
        curr = np.array(weights[layz])
        w.append(curr.reshape(L, L+1))
    w.append(np.array(weights[-1]))
    a = []
    z = [np.matmul(w[0], t)]
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

def sig(x):
    if x > 100:
        return 1
    if x < -100:
        return 0
    return 1 / (1 + math.exp(-x))