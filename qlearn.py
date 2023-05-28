from engine.GameEngine import GameEngine
from player.RandomAI import RandomAI
from player.QLearningAI import QLearningAI

def main():
    QAI1 = QLearningAI()
    QAI2 = QLearningAI(.05)
    QAI3 = QLearningAI(.2)
    QAIW = 0
    RandomW = 0
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI1)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI1:
            QAIW += 1
        else:
            RandomW += 1
    print("QAI1 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")
    QAIW = 0
    RandomW = 0
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI2)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI2:
            QAIW += 1
        else:
            RandomW += 1
    print("QAI2 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")
    QAIW = 0
    RandomW = 0
    for i in range(25000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI3)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI3:
            QAIW += 1
        else:
            RandomW += 1
    print("QAI3 won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")

if __name__ == '__main__':
    main()