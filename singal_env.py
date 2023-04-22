import random
import numpy as np,numpy.random


class SignalEachTimeGapEnv:

    def __init__(self,channel=9,last_state=[]):
        self.channel=channel
        self.last_state=last_state
        # 转移矩阵P[state][action] = [(p, next_state, reward, done)]包含下一个状态和奖励
        self.P=self.transfer()
        #当前干扰概率矩阵
        self.interference_p= np.random.dirichlet(np.ones(channel), size=1)[0]

        # 初始化传输强度列表  J1,J2,J3 乱序
        interference_intensity=[1,2,3]
        random.shuffle(interference_intensity)

        # 初始化传输强度列表  T1,T2,T3 乱序
        transfer_power=[1,2,3]
        random.shuffle(transfer_power)


    def transfer(self):
        change = [1,2,3,4,5,6,7,8,9]

    def createP(self,last_state):
        first_interference_p= max(self.interference_p)
        first_interference_index=self.interference_p.index(first_interference_p)

        self.interference_p[first_interference_index]=0
        second_interference_p=max(self.interference_p)
        second_interference_index=self.interference_p.index(second_interference_p)

        reward=[]
        #初始化奖励矩阵
        for i in range(1,self.channel+1):
            reward.append(100)

        #干扰的两个信道奖励为0
        reward[first_interference_index]=0
        reward[second_interference_index]=0


    def compute(P, rewards, gamma, states_num):
        rewards = np.array(rewards).reshape((-1, 1))  # 将rewards写成列向量形式
        value = np.dot(np.linalg.inv(np.eye(states_num, states_num) - gamma * P),
                       rewards)
        return value



