from engine.GameEngine import GameEngine
from player.RandomAI import RandomAI
from player.QLearningAI import QLearningAI

def main():
    QAI1 = QLearningAI()
    QAI2 = QLearningAI(.05)
    QAI3 = QLearningAI(.2)
    QAIW = 0
    RandomW = 0
    for i in range(10000000):
        engine1 = GameEngine()
        engine1.addPlayer(QAI3)
        randomAI = RandomAI()
        engine1.addPlayer(randomAI)
        winner = engine1.runGame()
        if winner == QAI3:
            QAIW += 1
        else:
            RandomW += 1
    print("QAI won " + str(QAIW) + " games vs Random won " + str(RandomW) + " games.")

if __name__ == '__main__':
    main()