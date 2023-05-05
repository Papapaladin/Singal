import copy
from singal_env import *

class PolicyIteration:

    def __init__(self, env, theta, gamma):
        self.env = env
        self.v = [[0] * self.env.channel for i in range(self.env.time_gap_amount)]
        change = self.env.change
        self.pi = [[[1 / change for i in range(change)] for channel in range(self.env.channel)] for time_gap in
                   range(self.env.time_gap_amount)]
        self.theta = theta
        self.gamma = gamma

    def policy_evaluation(self):
        cnt = 1  # 计数器
        while 1:
            max_diff = 0
            # new_v = [0] * self.env.channel * self.env.time_gap_amount
            new_v = [[0] * self.env.channel for i in range(self.env.time_gap_amount)]

            for time_gap in range(self.env.time_gap_amount):
                for channel in range(self.env.channel):
                    qsa_list = []  # 开始计算状态s下的所有Q(s,a)价值
                    for action in range(self.env.change):
                        qsa = 0
                        for res in self.env.P[time_gap][channel][action]:
                            p, next_state, reward = res
                            qsa += p * (reward + self.gamma * self.v[time_gap][channel])
                        qsa_list.append(self.pi[time_gap][channel][action] * qsa)
                    new_v[time_gap][channel] = sum(qsa_list)
                    max_diff = max(max_diff, abs(new_v[time_gap][channel] - self.v[time_gap][channel]))

            self.v = new_v
            if max_diff < self.theta: break
            cnt += 1

        print("策略评估进行%d轮后完成" % cnt)

    def policy_improvement(self):  # 策略提升
        for time_gap in range(self.env.time_gap_amount):
            for channel in range(self.env.channel):
                qsa_list=[]
                for action in range(self.env.change):
                    qsa=0
                    for res in self.env.P[time_gap][channel][action]:
                        p, next_state, reward = res
                        qsa += p * (reward + self.gamma * self.v[time_gap][channel])
                    qsa_list.append(qsa)
                maxq = max(qsa_list)
                cntq = qsa_list.count(maxq)
                self.pi[time_gap][channel] = [1 / cntq if q == maxq else 0 for q in qsa_list]

        print("策略提升完成")
        return self.pi

    def policy_iteration(self):  # 策略迭代
        while 1:
            self.policy_evaluation()
            old_pi = copy.deepcopy(self.pi)  # 将列表进行深拷贝,方便接下来进行比较
            new_pi = self.policy_improvement()
            if old_pi == new_pi: break

def print_agent(agent, action_meaning, interrupt=[], end=[]):
    print("状态价值：")
    for time_gap in range(agent.env.time_gap_amount):
        for channel in range(agent.env.channel):
            print('%6.6s' % ('%.3f' % agent.v[time_gap * agent.env.ncol + channel]),
                  end=' ')

    for time_gap in range(agent.env.time_gap_amount):
        for channel in range(agent.env.channel):

            # 一些特殊的状态,例如悬崖漫步中的悬崖
            if (time_gap * agent.env.channel + channel) in interrupt:
                print('****', end=' ')
            elif (time_gap * agent.env.channel + channel) in end:  # 目标状态
                print('EEEE', end=' ')
            else:
                a = agent.pi[time_gap * agent.env.channel + channel]
                pi_str = ''
                for k in range(len(action_meaning)):
                    pi_str += action_meaning[k] if a[k] > 0 else 'o'
                print(pi_str, end=' ')
        print()


env=SignalEachTimeGapEnv()
action_meaning=['channel_1','channel_2','channel_3','channel_4','channel_5','channel_6','channel_7','channel_8','channel_9']
theta=0.001
gamma=0.9
agent=PolicyIteration(env,theta,gamma)
agent.policy_iteration()
print_agent(agent,action_meaning,list(range(7,15)),[47])