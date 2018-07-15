from ABB120_FK_basic import ABB120_FK_basic as FK
import numpy as np
from kaveh_pso import pso

for SMR_num in range(1,4):

    Joints_angle_list=np.loadtxt('Measurements/joints_SMR_tool.txt')
    Target_position_list=np.loadtxt('Measurements/position_SMR_'+str(SMR_num)+'.txt')

    def func(v):
        y = 0
        for i in range(0, len(Target_position_list)):
            y += np.linalg.norm(Target_position_list[i]-FK(Joints_angle_list[i], v))
        return y

    LB=[-2000, -2000, -2000, -180, -180, -180, -300, -300, -300]
    UB=[+4000, +4000, +4000, +180, +180, +180, +400, +400, +400]

    solver = pso(func, 9, LB, UB, Max_It=400, n_Pop = 100)
    xopt, fopt=solver.run()

    print('*****************')
    print(' ')
    print('Error: ',  fopt)
    print('Robot Base:   ',xopt[0:6])
    print('SMR_'+str(SMR_num)+' Pose:     ',xopt[6:9])

    np.savetxt('Results/SMR_'+str(SMR_num)+'.txt',xopt)
