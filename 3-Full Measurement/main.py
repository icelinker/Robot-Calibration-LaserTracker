import sys
import os
from time import sleep
import numpy as np
sys.path.append('../LaserTracker/')
sys.path.append('../ConnectABB/')
import PyLaserTracker
from ABB_Socket import ABB_Socket

generated_joints=np.loadtxt('Input/generated_joints.txt')
generated_SMR_1=np.loadtxt('Input/generated_SMR_1.txt')
generated_SMR_2=np.loadtxt('Input/generated_SMR_2.txt')
generated_SMR_3=np.loadtxt('Input/generated_SMR_3.txt')
basic_SMRs=np.loadtxt('Input/position_SMR_base.txt')
base_1=basic_SMRs[0,:]
base_2=basic_SMRs[1,:]
base_3=basic_SMRs[2,:]

input("Please turn on Laser Tracker then press enter >>")
input("Please run the rapid file then press enter >>")
connection = ABB_Socket("192.168.125.1", 1025)
connection.SetTCPSpeed(50)

LT=PyLaserTracker.API()
sleep(3)
LT.Initialize()
LT.SetSamples(1000)

measured_joints=[]
measured_SMR_1=[]
measured_SMR_2=[]
measured_SMR_3=[]
measured_base_1=[]
measured_base_2=[]
measured_base_3=[]

for i in range(3,len(generated_joints)):
    connection.MoveAbsJ(generated_joints[i])
    print(generated_joints[i])
    measured_joints.append(connection.ReadJoints())
    LT.SetSMRDiameterPouces(1/2)
    #measured_SMR_1.append(LT.Find(generated_SMR_1[i][0], generated_SMR_1[i][1], generated_SMR_1[i][2]))
    measured_SMR_2.append(LT.Find(generated_SMR_2[i][0]+10, generated_SMR_2[i][1]+10, generated_SMR_2[i][2]))
    #measured_SMR_3.append(LT.Find(generated_SMR_3[i][0], generated_SMR_3[i][1], generated_SMR_3[i][2]))
    LT.SetSMRDiameterPouces(3/2)
    measured_base_1.append(LT.Find(base_1[0], base_1[1], base_1[2]))
    measured_base_2.append(LT.Find(base_2[0], base_2[1], base_2[2]))
    measured_base_3.append(LT.Find(base_3[0], base_3[1], base_3[2]))

    #np.savetxt('Output/measured_joints.txt', measured_joints)
    #np.savetxt('Output/measured_SMR_1.txt', measured_SMR_1)
    #np.savetxt('Output/measured_SMR_2.txt', measured_SMR_2)
    #np.savetxt('Output/measured_SMR_3.txt', measured_SMR_3)
    #np.savetxt('Output/measured_base_1.txt', measured_base_1)
    #np.savetxt('Output/measured_base_2.txt', measured_base_2)
    #np.savetxt('Output/measured_base_3.txt', measured_base_3)

connection.delete()
LT.Finalize()
