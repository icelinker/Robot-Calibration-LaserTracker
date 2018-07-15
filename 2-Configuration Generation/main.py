import pybullet as p
import time
import math
import numpy as np
from datetime import datetime
from time import sleep
import os
from Gen_joints import Gen_joints
os.system('cls')

p.connect(p.GUI)
groundId = p.loadURDF("models/Ground/plane.urdf",[0,0,0],useFixedBase=True)
kukaId = p.loadURDF("models/IRB120/model.urdf",[0,0,0.8],useFixedBase=True)
tableId = p.loadURDF("models/Table/table_square.urdf",[0,0,0],useFixedBase=True)

generated_joints=[]
generated_SMR_1=[]
generated_SMR_2=[]
generated_SMR_3=[]

def add_select(joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser):
    global generated_joints
    global generated_SMR_1
    global generated_SMR_2
    global generated_SMR_3

    generated_joints.append( joints )
    generated_SMR_1.append( SMR_1_wrt_laser )
    generated_SMR_2.append( SMR_2_wrt_laser )
    generated_SMR_3.append( SMR_3_wrt_laser )

def remove_select():
    global generated_joints
    global generated_SMR_1
    global generated_SMR_2
    global generated_SMR_3

    del(generated_joints[-1])
    del(generated_SMR_1[-1])
    del(generated_SMR_2[-1])
    del(generated_SMR_3[-1])

def check_collision(next_joints,last_joints,iter=100):
    global p
    global kukaId
    global tableId

    collision_check=0
    maxDist = 1
    for q in range(iter):
        #sleep(0.01)
        current_joints=(q/iter*(np.array(next_joints)-np.array(last_joints))+np.array(last_joints)).tolist()
        for j in range(0,6):
            p.resetJointState(kukaId,j,current_joints[j]*math.pi/180)

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
                break
        if collision_check == 1:
            break
    return collision_check

def save_all():
    global generated_joints
    global generated_SMR_1
    global generated_SMR_2
    global generated_SMR_3

    np.savetxt('Output/generated_joints.txt',np.array(generated_joints))
    np.savetxt('Output/generated_SMR_1.txt',np.array(generated_SMR_1))
    np.savetxt('Output/generated_SMR_2.txt',np.array(generated_SMR_2))
    np.savetxt('Output/generated_SMR_3.txt',np.array(generated_SMR_3))       

#***********************************************************
#***********************************************************
stay_loop=True
while stay_loop:
    joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser =Gen_joints()
    last_joints=joints
    collision_check = check_collision(last_joints,last_joints,iter=1)
    if collision_check==0:
        add_select(joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser)
        print(joints[3])
        stay_loop=False

while len(generated_joints)<1000 :
    print('************************')
    print('generated list length:  ',len(generated_joints))
    stay_loop=True
    i=0
    while stay_loop:
        i+=1

        joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser =Gen_joints()
        next_joints=joints
        collision_check = check_collision(next_joints,last_joints)

        if collision_check == 0:
            add_select(joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser)
            print(joints[3])
            last_joints=joints
            save_all()
            stay_loop=False

        if stay_loop==True and i>100:
            remove_select()
            last_joints=generated_joints[-1]
            stay_loop=False
            




