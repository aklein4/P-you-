
from os import DirEntry
from sympy import true

SOURCE = "data/data_fixed.txt"
DIRECTORY = "data/fixed_data"
PREFIX = "fixed_"

# second key is what is being held!!!!

def is_valid(key):
    for char in "qwertyuiopasdfghjklzxcvbnm ":
        if key==char:
            return True
    return False

def main():
    data = open(SOURCE, "r", encoding="utf-8")

    # get file format
    header = data.readline().strip().split(";")
    i_user = 0
    i_time = 0
    i_hold = 0
    i_key = 0
    for i in range(len(header)):
        if header[i].lower() == "userid":
            i_user = i
        if header[i].lower() == "d1d2":
            i_time = i
        if header[i].lower() == "d1u1":
            i_hold = i
        if header[i].lower() == "keycode":
            i_key = i

    # read and store better data
    curr_user = 0
    curr_user_data = []
    prev_key = "none"
    for line in data:
        info = line.strip().split(";")
        if int(info[i_user])!=curr_user:
            if curr_user != -1 and curr_user != 100 and curr_user != 0:
                dump = open(DIRECTORY+"/"+PREFIX+str(curr_user)+".txt", "w")
                for j in range(0,len(curr_user_data)):
                    set = curr_user_data[j]
                    try:
                        if is_valid(set[0]) and is_valid(set[1]) and set[2]!="" and set[3]!="":
                            if j != len(curr_user_data)-1:
                                dump.write(set[0]+","+set[1]+","+set[2]+","+set[3]+"\n")
                            else:
                                dump.write(set[0]+","+set[1]+","+set[2]+","+set[3])
                    except:
                        pass
                dump.close()
            prev_key = "none"
            curr_user_data = []
        if prev_key != "none":
            curr_user_data.append([prev_key,info[i_key],info[i_time],info[i_hold]])
        prev_key = info[i_key]
        curr_user = int(info[i_user])

    data.close()
        

if __name__ == "__main__":
    main()