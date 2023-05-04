import copy


class PolicyIteration:

    def __init__(self,env,theta,gamma):
        self.env=env
        self.v=[0]*self.env.channel*self.env.time_gap_amount
        change=self.env.change
        self.pi=[[[1/change for i in range(change)] for channel in range(self.env.channel)] for time_gap in range(self.env.time_gap_amount)]
        self.theta=theta
        self.gamma=gamma

    def policy_evaluation(self):
        cnt = 1  # 计数器
        while 1:
            max_diff = 0
            # new_v = [0] * self.env.channel * self.env.time_gap_amount
            new_v=[[0] for channel in self.env.channel]

            for time_gap in range(self.env.time_gap_amount):
                for channel in range(self.env.channel):
                    qsa_list = []  # 开始计算状态s下的所有Q(s,a)价值
                    for action in range(self.env.change):
                        qsa=0
                        for res in self.env.P[time_gap][channel][action]:
                            reward=res






                    qsa = 0
                    for res in self.env.P[s][a]:
                        p, next_state, r, done = res
                        qsa += p * (r + self.gamma * self.v[next_state] *
                                    (1 - done))
                        # 本章环境比较特殊,奖励和下一个状态有关,所以需要和状态转移概率相乘
                    qsa_list.append(self.pi[s][a] * qsa)
                new_v[s] = sum(qsa_list)  # 状态价值函数和动作价值函数之间的关系
                max_diff = max(max_diff, abs(new_v[s] - self.v[s]))
            self.v = new_v
            if max_diff < self.theta: break  # 满足收敛条件,退出评估迭代
            cnt += 1
        print("策略评估进行%d轮后完成" % cnt)
    def policy_improvement(self):  # 策略提升
        for s in range(self.env.nrow * self.env.ncol):
            qsa_list = []
            for a in range(4):
                qsa = 0
                for res in self.env.P[s][a]:
                    p, next_state, r, done = res
                    qsa += p * (r + self.gamma * self.v[next_state] *
                                (1 - done))
                qsa_list.append(qsa)
            maxq = max(qsa_list)
            cntq = qsa_list.count(maxq)  # 计算有几个动作得到了最大的Q值
            # 让这些动作均分概率
            self.pi[s] = [1 / cntq if q == maxq else 0 for q in qsa_list]
        print("策略提升完成")
        return self.pi

    def policy_iteration(self):  # 策略迭代
        while 1:
            self.policy_evaluation()
            old_pi = copy.deepcopy(self.pi)  # 将列表进行深拷贝,方便接下来进行比较
            new_pi = self.policy_improvement()
            if old_pi == new_pi: break







