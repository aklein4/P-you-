import os

DIRECTORIES = ["fixed_data", "free_data"]

letters = "qwertyuiopasdfghjklzxcvbnm "

def main():

    combos = {}
    for i in letters:
        for j  in letters:
            combos[(i,j)] = 0

    for direct in DIRECTORIES:
        for file in os.listdir(direct):
            data = open(direct+"/"+file, "r", encoding="utf-8")
            for line in data:
                key = line.strip().split(",")
                if key[0] == "":
                    key[0] = " "
                combos[(key[0],key[1])] += 1
            data.close()

    for key in combos:
        print(key, "=", combos[key])
    

if __name__ == "__main__":
    main()