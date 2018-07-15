import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

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
x=np.array(measured_base_1)-np.mean(np.array(measured_base_1),axis=0)

n_bins = 40

fig1 = plt.figure()

colors = ['red', 'blue', 'gray']
labels = ['x', 'y', 'z']
plt.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=labels)
plt.legend(prop={'size': 10})
plt.title('bars with legend')

plt.tight_layout()

#********************************************
x=np.array(measured_base_2)-np.mean(np.array(measured_base_2),axis=0)

n_bins = 40

fig2 = plt.figure()

colors = ['red', 'blue', 'gray']
labels = ['x', 'y', 'z']
plt.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=labels)
plt.legend(prop={'size': 10})
plt.title('bars with legend')

plt.tight_layout()

#********************************************
x=np.array(measured_base_3)-np.mean(np.array(measured_base_3),axis=0)
print(x)

n_bins = 40

fig3 = plt.figure()

colors = ['red', 'blue', 'gray']
labels = ['x', 'y', 'z']
plt.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=labels)
plt.legend(prop={'size': 10})
plt.title('bars with legend')

plt.tight_layout()

#********************************************
plt.show()
