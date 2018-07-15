import numpy as np


measured_joints=np.loadtxt('Input/measured_joints.txt').tolist()

measured_SMR_1=np.loadtxt('Input/measured_SMR_1.txt').tolist()
measured_SMR_2=np.loadtxt('Input/measured_SMR_2.txt').tolist()
measured_SMR_3=np.loadtxt('Input/measured_SMR_3.txt').tolist()

measured_base_1=np.loadtxt('Input/measured_base_1.txt').tolist()
measured_base_2=np.loadtxt('Input/measured_base_2.txt').tolist()
measured_base_3=np.loadtxt('Input/measured_base_3.txt').tolist()

base_mean_1=np.mean(np.array(measured_base_1),axis=0)
base_mean_2=np.mean(np.array(measured_base_2),axis=0)
base_mean_3=np.mean(np.array(measured_base_3),axis=0)


i=0
j=0
while i < len(measured_joints):

    if measured_base_1[i]==[0.0,0.0,0.0] or measured_base_2[i]==[0.0,0.0,0.0] or measured_base_3[i]==[0.0,0.0,0.0] or measured_SMR_1[i]==[0.0,0.0,0.0] or measured_SMR_2[i]==[0.0,0.0,0.0] or measured_SMR_3[i]==[0.0,0.0,0.0] \
        or np.linalg.norm(measured_base_1[i]-base_mean_1)>0.1 or np.linalg.norm(measured_base_2[i]-base_mean_2)>7 or np.linalg.norm(measured_base_3[i]-base_mean_3)>33:
        j+=1
        print('i = ',i,',   invalide data: ',j)
        del(measured_SMR_1[i]); del(measured_SMR_2[i]); del(measured_SMR_3[i])
        del(measured_base_1[i]); del(measured_base_2[i]); del(measured_base_3[i]); 
        del(measured_joints[i])
    else:
        i+=1

#********************************************
#********************************************

refined_SMR_1=[0]*len(measured_base_1)
refined_SMR_2=[0]*len(measured_base_2)
refined_SMR_3=[0]*len(measured_base_3)

for i in range(len(measured_joints)):
    vec_x=np.array(measured_base_1[i])-np.array(measured_base_2[i])/np.linalg.norm(np.array(measured_base_1[i])-np.array(measured_base_2[i]))
    vec_yp=np.array(measured_base_3[i])-np.array(measured_base_1[i])/np.linalg.norm(np.array(measured_base_3[i])-np.array(measured_base_1[i]))
    vec_z=np.cross(vec_x,vec_yp)
    vec_y=np.cross(vec_z,vec_x)
    R_L_T=np.transpose(np.vstack([vec_x, vec_y, vec_z]))
    H_L_T=np.eye(4)
    H_L_T[0:3,0:3]=R_L_T
    H_L_T[0:3,3]=np.array(measured_base_1[i])
    refined_SMR_1[i]= ( np.linalg.inv(H_L_T) @ np.hstack((measured_SMR_1[i],1.0)) )[0:3].tolist()
    refined_SMR_2[i]= ( np.linalg.inv(H_L_T) @ np.hstack((measured_SMR_2[i],1.0)) )[0:3].tolist()
    refined_SMR_3[i]= ( np.linalg.inv(H_L_T) @ np.hstack((measured_SMR_3[i],1.0)) )[0:3].tolist()


#********************************************
#********************************************

np.savetxt('Output/processed_joints.txt', measured_joints)
np.savetxt('Output/processed_SMR_1.txt', measured_SMR_1)
np.savetxt('Output/processed_SMR_2.txt', measured_SMR_2)
np.savetxt('Output/processed_SMR_3.txt', measured_SMR_3)
np.savetxt('Output/processed_SMR_1_wrt_base.txt', refined_SMR_1)
np.savetxt('Output/processed_SMR_2_wrt_base.txt', refined_SMR_2)
np.savetxt('Output/processed_SMR_3_wrt_base.txt', refined_SMR_3)
#np.savetxt('Output/processed_base_1.txt', measured_base_1)
#np.savetxt('Output/processed_base_2.txt', measured_base_2)
#np.savetxt('Output/processed_base_3.txt', measured_base_3)

