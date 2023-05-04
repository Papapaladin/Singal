import random
import numpy as np,numpy.random


class SignalEachTimeGapEnv:

    def __init__(self,channel=9,time_gap_amount=9,priori_kg=[]):
        self.prior_kg=priori_kg
        self.channel=channel
        self.change = channel
        self.time_gap_amount=time_gap_amount
        self.init_inter_p=[]
        for time_gap in range(time_gap_amount):
            self.init_inter_p.append( np.random.dirichlet(np.ones(channel), size=1)[0])


        # 初始化传输强度列表  J1,J2,J3 乱序
        interference_intensity=[1,2,3]
        random.shuffle(interference_intensity)

        # 初始化传输强度列表  T1,T2,T3 乱序
        transfer_power=[1,2,3]
        random.shuffle(transfer_power)

    def createP(self):
        #初始化
        P=[[[] for i in range(self.channel)] for j in range(self.time_gap_amount)]

        # channel 种动作 保持原信道不变 也是一种动作

        for time_gap in range(self.time_gap_amount):

            time_gap_interference = self.init_inter_p[time_gap]
            first_interference_p = max(time_gap_interference)
            first_interference_index = time_gap_interference.index(first_interference_p)

            time_gap_interference[first_interference_index] = 0
            second_interference_p = max(time_gap_interference)
            second_interference_index = time_gap_interference.index(second_interference_p)

            for channel in range(self.channel):
                for change in range(self.change):
                    if change==first_interference_index+1 or change==second_interference_index+1:
                        reward=0
                    else:
                        reward=1

                    P[time_gap][channel][change]=reward

        return P

    def compute(P, rewards, gamma, states_num):
        rewards = np.array(rewards).reshape((-1, 1))  # 将rewards写成列向量形式
        value = np.dot(np.linalg.inv(np.eye(states_num, states_num) - gamma * P),
                       rewards)
        return value


