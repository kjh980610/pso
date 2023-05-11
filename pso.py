import numpy as np
import cal_yan
import random

class pso:
    def __init__(self, 
                 init_l = np.array([50, 41.5, 61.9, 39.3, 55.8, 40.1, 39.4, 36.7, 65.7, 49]),
                 p_num = 10,
                 max_iter = 10 
                 ):
        self.link = init_l
        self.p_num = p_num
        self.max_iter = max_iter
        self.pbest = np.zeros((self.p_num,11))
        self.gbest = np.zeros(11)

    def run(self):
        parti = np.zeros((self.p_num,10))
        vel = np.zeros((self.p_num,10))
        pre_vel = np.zeros((self.p_num,10))

        for d in range(self.p_num) :
            for j in range(10) :
                parti[d,j]= self.link[j] #* (1.1 - random.random()*0.2)
            pre_vel[d] = self.link*0.005
        vel = pre_vel+0

        w = 1
        a = 0.8
        c = 1.5
        f = 0
        print('------시작------')
        for i in range(self.max_iter):
            w = w * a
            if (i+1)%5 == 0 :
                print(f'@@@@@@@@@@@@{i+1}번째 진행중@@@@@@@@@@@@@@@')

            for d in range(self.p_num):
                e_cnt=0
                while e_cnt < 15:
                    try:
                        f = self.cal_obj_func(parti[d])
                    except Exception as e:
                        e_cnt = e_cnt+1
                        print(e)
                        parti[d] = parti[d] - vel[d]
                        for k in range(10):
                            vel[d,k] = w*pre_vel[d,k] + c*random.random()*(self.pbest[d,k]-parti[d,k]) + c*random.random()*(self.gbest[k]-parti[d,k])
                        parti[d] = parti[d] + vel[d]
                    else:
                        pre_vel[d]=vel[d]+0
                        break
                if e_cnt > 10:
                        print(f'{i+1}번째 시행 {d+1}번 입자 error {e_cnt}')
                if f > self.pbest[d,-1] :
                    self.pbest[d,:10] = parti[d]
                    self.pbest[d,-1] = f
                if f > self.gbest[-1] :
                    self.gbest[:10] = parti[d]
                    self.gbest[-1] = f
                for k in range(10):
                    vel[d,k] = w*pre_vel[d,k] + c*random.random()*(self.pbest[d,k]-parti[d,k]) + c*random.random()*(self.gbest[k]-parti[d,k])

            parti = parti + vel


        print(f'gbest: {self.gbest[:10]}')
        print(cal_yan.cal_yan(self.gbest[:10]))
        return self.gbest[:10]


    def cal_obj_func(self,l) :
        f = cal_yan.cal_yan(l)
        w = np.array([1,10,-10,-1])
        obj_func = 0

        for i in range(4):
            obj_func = obj_func +f[i] * w[i]

        return obj_func

