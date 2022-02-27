
USER_FILE = "user"

P_HACKER = 0.4

def check(times):
    return 0.9

def get_password():
    f = open(USER_FILE+".txt", "r")
    password = f.readline().strip()
    f.close()
    return password