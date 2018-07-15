import numpy as np
from math import pi
from RoboDesk import rotx, roty, rotz
from IK_IRB120 import IK_IRB120
from time import sleep
import random
from math import sin, cos, atan2, pi
import numpy as np


def Random_Pose(P, BasePose_wrp_LaserTrackerH, H_tool_wrt_flange):
    temp = np.linalg.inv(BasePose_wrp_LaserTrackerH)
    P_L_wrt_base = temp[0:3, 3]
    axes_z_p = (P_L_wrt_base-P)/np.linalg.norm(P_L_wrt_base-P)
    rndV = np.random.rand(3)
    axes_y_p = np.cross(rndV, axes_z_p) / np.linalg.norm(np.cross(rndV, axes_z_p))
    axes_x_p = np.cross(axes_y_p, axes_z_p)
    H_tool_wrt_base = np.stack((axes_x_p, axes_y_p, axes_z_p, P),axis=1)
    H_tool_wrt_base = np.vstack((H_tool_wrt_base,[0, 0, 0, 1]))
    H_flange_wrt_base = H_tool_wrt_base @ np.linalg.inv(H_tool_wrt_flange)
    return H_flange_wrt_base

def Gen_joints():
    SMR_1 = np.loadtxt('Input/SMR_1.txt')
    SMR_2 = np.loadtxt('Input/SMR_2.txt')
    SMR_3 = np.loadtxt('Input/SMR_3.txt')

    Base_wrp_L_position = SMR_3[0:3]
    Base_wrp_L_euler = SMR_3[3:6]*pi/180

    SMR1_wrt_Flange = SMR_1[6:9]
    SMR2_wrt_Flange = SMR_2[6:9]
    SMR3_wrt_Flange = SMR_3[6:9]

    H_0_wrt_L = np.eye(4)
    R_0_wrt_L = rotz(Base_wrp_L_euler[0]) @  roty( Base_wrp_L_euler[1]) @ rotx(Base_wrp_L_euler[2])
    H_0_wrt_L[0:3, 0:3] = R_0_wrt_L
    H_0_wrt_L[0:3, 3] = [Base_wrp_L_position[0], Base_wrp_L_position[1], Base_wrp_L_position[2]]

    SMRs_wrp_Flange = np.stack(
        (SMR1_wrt_Flange, SMR2_wrt_Flange, SMR3_wrt_Flange), axis=1)
    MeanPoint = np.mean(SMRs_wrp_Flange, axis=0)

    axes_z_tool_wrt_flange = np.cross(SMRs_wrp_Flange[:, 2]-SMRs_wrp_Flange[:, 0], SMRs_wrp_Flange[:, 1]-SMRs_wrp_Flange[:, 0])
    axes_z_tool_wrt_flangeN = axes_z_tool_wrt_flange / np.linalg.norm(axes_z_tool_wrt_flange)
    axes_x_tool_wrt_flange = (SMRs_wrp_Flange[:, 2]-SMRs_wrp_Flange[:, 0])
    axes_x_tool_wrt_flangeN = axes_x_tool_wrt_flange / np.linalg.norm(axes_x_tool_wrt_flange)
    axes_y_tool_wrt_flangeN = np.cross(axes_z_tool_wrt_flangeN, axes_x_tool_wrt_flangeN)

    H_flange_tool = np.eye(4)
    H_flange_tool[0:3, 0:4] = np.transpose(np.vstack([axes_x_tool_wrt_flangeN, axes_y_tool_wrt_flangeN, axes_z_tool_wrt_flangeN, MeanPoint]))

    positions_min = np.array([-400, -1000, 100])
    positions_max = np.array([1000, 1000, 2000])

    stay_loop=True

    while stay_loop:
        P = np.multiply(np.random.rand(3), (positions_max-positions_min))+positions_min
        New_H_flange_wrt_base = Random_Pose(P, H_0_wrt_L, H_flange_tool)
        solutions = IK_IRB120(New_H_flange_wrt_base)

        if solutions is not None:
            solution_number =random.randint(0,len(solutions)-1)
            joints=solutions[solution_number]

            temp = H_0_wrt_L @ New_H_flange_wrt_base @ np.hstack((SMRs_wrp_Flange[:,0],1))
            SMR_1_wrt_laser = np.transpose(temp[0:3]).tolist()

            temp = H_0_wrt_L @ New_H_flange_wrt_base @ np.hstack((SMRs_wrp_Flange[:,1],1))
            SMR_2_wrt_laser  = np.transpose(temp[0:3]).tolist()

            temp = H_0_wrt_L @ New_H_flange_wrt_base @ np.hstack((SMRs_wrp_Flange[:,2],1))
            SMR_3_wrt_laser  = np.transpose(temp[0:3]).tolist()
            stay_loop=False

    return joints, SMR_1_wrt_laser , SMR_2_wrt_laser , SMR_3_wrt_laser 
