import numpy

USER_FILE = "user"

def create(password, times):
    f = open(USER_FILE+".txt", "w")
    f.write(password+"\n")
    for set in times:
        line = ""
        for t in set:
            line += ","+str(round(t))
        line += "\n"
        f.write(line[1:])
    f.close()