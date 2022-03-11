import main
import create_password
import check_password
import numpy as np
import random
from matplotlib import pyplot
import math
import os
import scipy.stats

N_TESTS = 10000
CREATE = True
P_HACKER = 0.4

def main_test():

    f = open("tests/user_tests/adam_klein.txt", "r")
    password = f.readline().strip("\n")

    weights = []
    for line in f:
        weights.append(line.strip().split(","))
    f.close()
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j] = float(weights[i][j])

    combos = create_password.get_combos(password)
    data = create_password.get_data(combos, password)

    not_me = []

    for set in data:
        not_me.append(math.log10(create_password.feed(password, weights, set)))

    not_mean = np.average(not_me)
    not_std = np.std(not_me)

    me = []
    f = open("my_tests.txt", "r")
    for line in f:
        me.append(math.log10(float(line.strip().split(",")[1])))
    f.close()

    me_mean = np.average(me)
    me_std = np.std(me)

    x = np.linspace(-3, 0, 100)
    y_me = scipy.stats.norm.pdf(x, me_mean, me_std)
    y_not = scipy.stats.norm.pdf(x, not_mean, not_std)
    y_mixed = y_me*(1-P_HACKER)/(y_me*(1-P_HACKER)+y_not*P_HACKER)
    y_mixed2 = y_me*(1-.1)/(y_me*(1-.1)+y_not*.1)
    y_mixed3 = y_me*(1-.9)/(y_me*(1-.9)+y_not*.9)
    pyplot.plot(x, scipy.stats.norm.pdf(x, me_mean, me_std), 'Green')
    pyplot.plot(x, scipy.stats.norm.pdf(x, not_mean, not_std), 'Red')
    pyplot.plot(x, y_mixed, 'Blue')
    pyplot.plot(x, y_mixed2, 'Blue')
    pyplot.plot(x, y_mixed3, 'Blue')
    pyplot.title("Example Normal Curves and Bayes Output")
    pyplot.show()
    return

    not_dists = []
    for file in os.listdir("tests/input_data/adam_klein_tests"):
        dis = []
        f = open("tests/input_data/adam_klein_tests/"+file, "r")
        for line in f:
            val = math.log10(float(line.strip().split(",")[1]))
            dis.append(
                scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)/(
                    scipy.stats.norm.pdf(val,loc=not_mean,scale=not_std)*P_HACKER+scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)
                    )
                )
        f.close()
        not_dists.append(dis)

    me_dist = []
    for val in me:
        me_dist.append(
            scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)/(
                scipy.stats.norm.pdf(val,loc=not_mean,scale=not_std)*P_HACKER+scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)
                )
            )

    fake_outcomes = []
    for n in range(N_TESTS):
        test_times = []
        for i in range(len(password)-1):
            test_times.append(random.randint(50,300))
        for i in range(len(password)-1):
            test_times.append(random.randint(50,150))
        divv = sum(test_times[0:len(password)])
        for i in range(len(test_times)):
            test_times[i] / divv
        test_times.insert(0,1)
        val = math.log10(check_password.feed(password, weights, test_times))
        fake_outcomes.append(
            scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)/(
                scipy.stats.norm.pdf(val,loc=not_mean,scale=not_std)*P_HACKER+scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)
                )
            )

    fake_outcomes2 = []
    for n in range(N_TESTS):
        test_times = []
        for i in range(len(password)-1):
            test_times.append(random.randint(50,500))
        for i in range(len(password)-1):
            test_times.append(random.randint(50,500))
        divv = sum(test_times[0:len(password)])
        for i in range(len(test_times)):
            test_times[i] / divv
        test_times.insert(0,1)
        val = math.log10(check_password.feed(password, weights, test_times))
        fake_outcomes2.append(
            scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)/(
                scipy.stats.norm.pdf(val,loc=not_mean,scale=not_std)*P_HACKER+scipy.stats.norm.pdf(val,loc=me_mean,scale=me_std)*(1-P_HACKER)
                )
            )

    fig, ((ax1, ax2), (ax3, ax4),(ax5, ax6),(ax7, ax8)) = pyplot.subplots(4, 2)
    fig.suptitle("P(You) Testing Outcomes")
    ax1.hist(me_dist, bins=25, range=(0,1), density=True, rwidth=1, color='Green')
    ax2.hist(not_dists[0], bins=25, range=(0,1), density=True, rwidth=1)
    ax3.hist(not_dists[1], bins=25, range=(0,1), density=True, rwidth=1)
    ax4.hist(not_dists[2], bins=25, range=(0,1), density=True, rwidth=1)
    ax5.hist(not_dists[3], bins=25, range=(0,1), density=True, rwidth=1)
    ax6.hist(not_dists[4], bins=25, range=(0,1), density=True, rwidth=1)
    ax7.hist(fake_outcomes, bins=25, range=(0,1), density=True, rwidth=1, color = 'Red')
    ax8.hist(fake_outcomes2, bins=25, range=(0,1), density=True, rwidth=1, color='Red')
    pyplot.show()

    # test_data = ADAMKLEIN
    # if CREATE:
    #     create_password.create(test_data["password"], test_data["data"])

    # fake_outcomes = []
    # for n in range(N_TESTS):
    #     test_times = []
    #     for i in range(len(test_data["password"])-1):
    #         test_times.append(random.randint(100,300))
    #     for i in range(len(test_data["password"])-1):
    #         test_times.append(random.randint(50,150))
    #     fake_outcomes.append(math.log10(check_password.check(test_times)))

    # true_outcomes = []
    # for set in test_data["tests"]:
    #     true_outcomes.append(math.log10(check_password.check(set)))

    # pyplot.hist([fake_outcomes, true_outcomes], bins=100, range=(-3,0), density=True, rwidth=1)
    # pyplot.axvline(math.log10(0.5), color='k', linestyle='dashed', linewidth=1)
    # pyplot.show()
    # return

ADAMKLEIN = {
    "password": "adamklein",
    "data": [
        [219.81048583984375, 123.97050857543945, 140.86198806762695, 228.48081588745117, 78.13739776611328, 281.3756465911865, 93.53113174438477, 204.0712833404541, 93.81651878356934, 92.65851974487305, 78.51958274841309, 62.67905235290527, 93.80650520324707, 109.4052791595459, 77.90160179138184, 62.55292892456055], 
        [227.47349739074707, 125.08034706115723, 116.9588565826416, 202.96621322631836, 78.32932472229004, 243.01505088806152, 109.39860343933105, 188.431978225708, 77.81338691711426, 62.65664100646973, 85.57271957397461, 62.520503997802734, 93.92428398132324, 70.98865509033203, 78.155517578125, 78.12952995300293],
        [235.42022705078125, 139.74571228027344, 141.79158210754395, 219.39349174499512, 62.47091293334961, 259.4292163848877, 109.41576957702637, 203.2909393310547, 78.31668853759766, 77.24189758300781, 94.97356414794922, 62.65521049499512, 78.09591293334961, 109.55095291137695, 78.26519012451172, 62.673091888427734],
        [230.81064224243164, 156.2788486480713, 130.25236129760742, 218.6896800994873, 93.78457069396973, 265.40112495422363, 93.96910667419434, 218.69945526123047, 109.5728874206543, 78.13906669616699, 98.81734848022461, 77.9573917388916, 78.14502716064453, 109.16733741760254, 78.2923698425293, 93.51587295532227],
        [237.22290992736816, 145.2810764312744, 109.3747615814209, 203.05514335632324, 62.53933906555176, 261.37661933898926, 108.9334487915039, 109.5418930053711, 93.59407424926758, 67.00634956359863, 78.1545639038086, 78.10354232788086, 93.71018409729004, 109.36093330383301, 93.31011772155762, 93.92118453979492],
        [219.47264671325684, 139.75143432617188, 109.16256904602051, 188.88163566589355, 92.65446662902832, 251.0673999786377, 92.74029731750488, 140.68961143493652, 93.60027313232422, 77.27384567260742, 78.06730270385742, 78.61661911010742, 108.49142074584961, 93.73784065246582, 61.567068099975586, 78.20558547973633],
        [252.05659866333008, 156.03041648864746, 93.82152557373047, 216.09973907470703, 71.25473022460938, 204.71787452697754, 125.86402893066406, 163.88726234436035, 78.14431190490723, 62.36433982849121, 62.53695487976074, 78.07040214538574, 68.1915283203125, 76.17759704589844, 86.53497695922852, 62.52264976501465],
        [227.677583694458, 156.94737434387207, 124.79925155639648, 203.25684547424316, 93.6884880065918, 214.6892547607422, 134.89198684692383, 187.38698959350586, 78.0034065246582, 78.76777648925781, 93.49870681762695, 62.546491622924805, 109.31587219238281, 78.94754409790039, 72.36099243164062, 62.46161460876465],
        [234.5564365386963, 155.9762954711914, 132.7195167541504, 218.77598762512207, 93.52302551269531, 266.68310165405273, 125.03337860107422, 140.87224006652832, 78.11522483825684, 62.25728988647461, 70.1904296875, 62.49427795410156, 93.52302551269531, 93.82963180541992, 92.74697303771973, 47.00875282287598],
        [219.60806846618652, 124.36938285827637, 125.31852722167969, 234.59601402282715, 94.6047306060791, 210.42990684509277, 109.52305793762207, 202.99363136291504, 77.98194885253906, 77.61001586914062, 78.46522331237793, 62.47520446777344, 101.88150405883789, 85.60633659362793, 62.61324882507324, 62.44921684265137]
        ],
    "tests": [
        [227.5073528289795, 93.42050552368164, 140.61307907104492, 216.19534492492676, 70.04189491271973, 187.67762184143066, 109.02833938598633, 93.90497207641602, 86.54379844665527, 62.041282653808594, 109.36641693115234, 78.16410064697266, 85.71410179138184, 62.5452995300293, 77.911376953125, 93.90497207641602],
        [211.9436264038086, 93.60361099243164, 151.89385414123535, 217.74673461914062, 19.750118255615234, 167.50359535217285, 141.41297340393066, 94.08140182495117, 97.00727462768555, 62.51788139343262, 93.9335823059082, 93.39737892150879, 70.28746604919434, 113.47746849060059, 94.37322616577148, 78.57799530029297],
        [244.9946403503418, 117.49958992004395, 140.6252384185791, 218.7345027923584, 78.10473442077637, 218.827486038208, 109.22527313232422, 93.72782707214355, 88.73963356018066, 70.3890323638916, 78.1099796295166, 62.471628189086914, 93.6422348022461, 93.54877471923828, 93.53446960449219, 93.72782707214355],
        [203.3236026763916, 109.21478271484375, 140.52677154541016, 186.9649887084961, 119.04478073120117, 164.72744941711426, 106.93597793579102, 78.17196846008301, 78.17316055297852, 62.232017517089844, 62.44206428527832, 61.6610050201416, 111.1454963684082, 70.87850570678711, 90.80362319946289, 78.17196846008301],
        [187.31927871704102, 62.315940856933594, 140.80238342285156, 218.83225440979004, 77.98099517822266, 165.45724868774414, 124.88365173339844, 77.94475555419922, 93.59169006347656, 62.315940856933594, 109.36784744262695, 78.08709144592285, 109.15017127990723, 109.69376564025879, 93.65606307983398, 77.94475555419922],
        [212.3279571533203, 108.47687721252441, 140.5651569366455, 219.5889949798584, 80.5821418762207, 216.1717414855957, 126.56784057617188, 87.79239654541016, 78.2783031463623, 45.94874382019043, 78.02653312683105, 62.505245208740234, 97.0609188079834, 75.25229454040527, 78.19795608520508, 78.04417610168457],
        [203.2034397125244, 93.6441421508789, 109.52210426330566, 187.49332427978516, 46.880483627319336, 156.92734718322754, 109.20596122741699, 87.2185230255127, 109.55524444580078, 78.0324935913086, 93.87874603271484, 78.11760902404785, 78.29523086547852, 94.28644180297852, 77.98433303833008, 87.2185230255127],
        [187.62946128845215, 93.76287460327148, 124.82666969299316, 187.8035068511963, 62.20841407775879, 150.60067176818848, 93.90950202941895, 62.827348709106445, 78.31764221191406, 78.06825637817383, 109.34281349182129, 62.6988410949707, 77.96239852905273, 93.86038780212402, 78.28760147094727, 62.827348709106445],
        [203.25994491577148, 93.58072280883789, 140.50579071044922, 203.21083068847656, 78.10735702514648, 243.43538284301758, 78.12094688415527, 93.58859062194824, 93.74833106994629, 77.79669761657715, 109.24673080444336, 62.612295150756836, 93.77288818359375, 87.10432052612305, 93.62936019897461, 93.58859062194824],
        [296.7720031738281, 124.82714653015137, 124.99403953552246, 194.34213638305664, 63.75908851623535, 208.1007957458496, 93.85490417480469, 94.95043754577637, 93.59049797058105, 62.419891357421875, 93.79410743713379, 62.4079704284668, 79.40673828125, 93.58882904052734, 84.9614143371582, 94.95043754577637]
    ]
}

main_test()