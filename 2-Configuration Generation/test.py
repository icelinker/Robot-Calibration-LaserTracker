import pybullet as p
import time
import math
import numpy as np
from datetime import datetime


generated_joints=np.loadtxt('Output/generated_joints.txt')
generated_SMR_1=np.loadtxt('Output/generated_SMR_1.txt')
generated_SMR_2=np.loadtxt('Output/generated_SMR_2.txt')
generated_SMR_3=np.loadtxt('Output/generated_SMR_3.txt')


p.connect(p.GUI)
groundId = p.loadURDF("models/Ground/plane.urdf",[0,0,0],useFixedBase=True)
kukaId = p.loadURDF("models/IRB120/model.urdf",[0,0,0.8],useFixedBase=True)
tableId = p.loadURDF("models/Table/table_square.urdf",[0,0,0],useFixedBase=True)

print(len(generated_joints))
last_joints=generated_joints[0,:]

for i in range(1,len(generated_joints)):
    print('Conf num: ', i)
    #p.stepSimulation()
    next_joints=generated_joints[i,:]
    collision_check = 0
    time.sleep(0.01)
    for q in range(0,100):
        time.sleep(0.001)
        current_joints=q/100*(next_joints-last_joints)+last_joints
        for j in range(0,6):
            #print(joints_list[i][j]*math.pi/180)
            p.resetJointState(kukaId,j,current_joints[j]*math.pi/180)
        maxDist = 1

        dist=[]
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=-1, bodyB=kukaId, linkIndexB=1, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=-1, bodyB=kukaId, linkIndexB=2, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=-1, bodyB=kukaId, linkIndexB=3, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=-1, bodyB=kukaId, linkIndexB=4, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=-1, bodyB=kukaId, linkIndexB=5, distance=maxDist)[0][8])

        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=0, bodyB=kukaId, linkIndexB=2, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=0, bodyB=kukaId, linkIndexB=3, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=0, bodyB=kukaId, linkIndexB=4, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=0, bodyB=kukaId, linkIndexB=5, distance=maxDist)[0][8])

        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=1, bodyB=kukaId, linkIndexB=3, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=1, bodyB=kukaId, linkIndexB=4, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=1, bodyB=kukaId, linkIndexB=5, distance=maxDist)[0][8])

        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=2, bodyB=kukaId, linkIndexB=4, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=2, bodyB=kukaId, linkIndexB=5, distance=maxDist)[0][8])

        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=3, bodyB=kukaId, linkIndexB=5, distance=maxDist)[0][8])

        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=2, bodyB=tableId, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=3, bodyB=tableId, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=4, bodyB=tableId, distance=maxDist)[0][8])
        dist.append(p.getClosestPoints(bodyA=kukaId, linkIndexA=5, bodyB=tableId, distance=maxDist)[0][8])

        collision_index=[[-1,1], [-1,2], [-1,3], [-1,2], [-1,5],
                         [0,2], [0,3], [0,4], [0,5],
                         [1,3], [1,4], [1,5],
                         [2, 4], [2,5],
                         [3, 5],
                         [-10, 2], [-10, 3], [-10, 4], [-10, 5]]

        for k in range(0,len(dist)):
            if dist[k]<0.001:
                collision_check = 1
                #p.changeVisualShape(tableId, -1, rgbaColor=[1, 1, 0, 1])
                #if collision_index[k][1]==-10:
                    #p.changeVisualShape(kukaId, linkIndex=collision_index[k][1], rgbaColor=[1,0,0,1])
                    #p.changeVisualShape(tableId, rgbaColor=[1, 0, 0, 1])
                    #p.changeVisualShape(kukaId, rgbaColor=[1, 0, 0, 1])
                #else:
                    #p.changeVisualShape(kukaId, rgbaColor=[1, 0, 0, 1])
                    #p.changeVisualShape(kukaId, linkIndex=collision_index[k][0], rgbaColor=[1,0,0,1])
                    #p.changeVisualShape(kukaId, linkIndex=collision_index[k][1], rgbaColor=[1, 0, 0, 1])


    if collision_check==1:
        print("collision")

    last_joints=next_joints
