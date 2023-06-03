from engine.GameEngine import GameEngine
from player.RandomAI import RandomAI
from player.QLearningAI import QLearningAI
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

def main():
    QAI1 = QLearningAI()
    QAI2 = QLearningAI(.05)
    QAI3 = QLearningAI(.2)
    QAIW = 0
    RandomW = 0
    count = 0
    batchQAIW = 0
    batchRandomW = 0
    xaxisArray = []
    plt.title("Q Learning Graph")
    plt.xlabel("Games Played")
    plt.ylabel("QAI win %")
    percentArray1 = []
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI1)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI1:
            QAIW += 1
            batchQAIW += 1
        else:
            RandomW += 1
            batchRandomW += 1
        count += 1
        if count % 250000 == 0:
            percentArray1.append(batchQAIW/(batchQAIW+batchRandomW))
            xaxisArray.append(count)
            batchQAIW = 0
            batchRandomW = 0
    print("QAI1 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")
    QAIW = 0
    RandomW = 0
    batchQAIW = 0
    batchRandomW = 0
    percentArray2 = []
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI2)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI2:
            QAIW += 1
            batchQAIW += 1
        else:
            RandomW += 1
            batchRandomW += 1
        count += 1
        if count % 250000 == 0:
            percentArray2.append(batchQAIW/(batchQAIW+batchRandomW))
            batchQAIW = 0
            batchRandomW = 0
    print("QAI2 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")
    QAIW = 0
    RandomW = 0
    batchQAIW = 0
    batchRandomW = 0
    percentArray3 = []
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI3)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI3:
            QAIW += 1
            batchQAIW += 1
        else:
            RandomW += 1
            batchRandomW += 1
        count += 1
        if count % 250000 == 0:
            percentArray3.append(batchQAIW/(batchQAIW+batchRandomW))
            batchQAIW = 0
            batchRandomW = 0
    print("QAI3 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")
    plt.plot(xaxisArray, percentArray1, color="red", label="e = .10", alpha=.4)
    plt.plot(xaxisArray, percentArray2, color="blue", label="e = .05", alpha=.4)
    plt.plot(xaxisArray, percentArray3, color="green", label="e = .20", alpha=.4)
    plt.legend(loc="lower right")
    plt.show()
    res11 = dict(sorted(QAI1.Q.items(), key=itemgetter(1), reverse=True)[:5])
    res12 = dict(sorted(QAI1.Q.items(), key=itemgetter(1), reverse=False)[:5])
 
    print("The top 5 state/action pairs for e = .10 are " + str(res11))
    print()
    print("The bottom 5 state/action pairs for e = .10 are " + str(res12))
    print()

    res21 = dict(sorted(QAI2.Q.items(), key=itemgetter(1), reverse=True)[:5])
    res22 = dict(sorted(QAI2.Q.items(), key=itemgetter(1), reverse=False)[:5])
 
    print("The top 5 state/action pairs for e = .05 are " + str(res21))
    print()
    print("The bottom 5 state/action pairs for e = .05 are " + str(res22))
    print()

    res31 = dict(sorted(QAI3.Q.items(), key=itemgetter(1), reverse=True)[:5])
    res32 = dict(sorted(QAI3.Q.items(), key=itemgetter(1), reverse=False)[:5])
 
    print("The top 5 state/action pairs for e = .20 are " + str(res31))
    print()
    print("The bottom 5 state/action pairs for e = .20 are " + str(res32))

if __name__ == '__main__':
    main()