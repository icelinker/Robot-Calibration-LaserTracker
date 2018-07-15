from math import sqrt
from random import uniform, random
import numpy as np
from copy import deepcopy

class empty_particle:
    def __init__(self, varsize):
        self.Position = np.array([0 for _ in range(varsize)])
        self.Cost = 0
        self.Velocity = np.array([0 for _ in range(varsize)])
        self.Best_Cost = 10
        self.Best_Position = np.array([0 for _ in range(varsize)])

class pso:
    def __init__(self,fnc, Var_Size, Var_Min, Var_Max,Max_It=4000,n_Pop = 20,phi_1 = 2.05,phi_2 = 2.05):
        self.CostFunction=fnc
        self.VarSize=Var_Size
        self.VarMin=np.array(Var_Min)
        self.VarMax=np.array(Var_Max)

        self.MaxIt = Max_It
        self.nPop = n_Pop
        phi = phi_1 + phi_2
        chi = 2 / (phi - 2 + sqrt(phi ** 2 - 4 * phi))
        self.w = chi
        self.wdamp = 1
        self.c1 = chi * phi_1
        self.c2 = chi * phi_2
        self.VelMax = 0.1 * (self.VarMax - self.VarMin)
        self.VelMin = -self.VelMax
        self.particles=[]
        for _ in range(self.nPop):
            self.particles.append(empty_particle(self.VarSize))

        self.GlobalBest_Position = np.array([0 for _ in range(self.VarSize)])
        self.GlobalBest_Cost = 1e20


    def init(self):
        for i in range(self.nPop):
            self.particles[i].Position = [uniform(self.VarMin[ii], self.VarMax[ii]) for ii in range(self.VarSize)]
            self.particles[i].Velocity = [0 for _ in range(self.VarSize)]
            self.particles[i].Cost = self.CostFunction(self.particles[i].Position)
            self.particles[i].Best_Position = self.particles[i].Position
            self.particles[i].Best_Cost = self.particles[i].Cost

            if self.particles[i].Best_Cost < self.GlobalBest_Cost:
                self.GlobalBest_Cost = deepcopy(self.particles[i].Best_Cost)
                self.GlobalBest_Position = deepcopy(self.particles[i].Best_Position)

    def run(self):
        self.init()
        for it in range(self.MaxIt):
            for i in range(self.nPop):
                for j in range(self.VarSize):
                    self.particles[i].Velocity[j] = self.w * self.particles[i].Velocity[j] \
                        + self.c1 * random() * (self.particles[i].Best_Position[j] - self.particles[i].Position[j])\
                        + self.c2 * random() * (self.GlobalBest_Position[j] - self.particles[i].Position[j])

                    self.particles[i].Velocity[j] = max(self.particles[i].Velocity[j], self.VelMin[j])
                    self.particles[i].Velocity[j] = min(self.particles[i].Velocity[j], self.VelMax[j])
                    self.particles[i].Position[j] = self.particles[i].Position[j] + self.particles[i].Velocity[j]
                    if (self.particles[i].Position[j] < self.VarMin[j] or self.particles[i].Position[j] > self.VarMax[j]):
                        self.particles[i].Velocity[j] = -self.particles[i].Velocity[j]
                    self.particles[i].Position[j] = max(self.particles[i].Position[j], self.VarMin[j])
                    self.particles[i].Position[j] = min(self.particles[i].Position[j], self.VarMax[j])

                self.particles[i].Cost = self.CostFunction(self.particles[i].Position)

                if self.particles[i].Cost < self.particles[i].Best_Cost:
                    self.particles[i].Best_Position = deepcopy(self.particles[i].Position)
                    self.particles[i].Best_Cost = deepcopy(self.particles[i].Cost)

                if self.particles[i].Best_Cost < self.GlobalBest_Cost:
                    self.GlobalBest_Position = deepcopy(self.particles[i].Best_Position)
                    self.GlobalBest_Cost = deepcopy(self.particles[i].Best_Cost)

            print('Iteration: ', it, '   CostFunction: ', self.CostFunction(self.GlobalBest_Position))

        return self.GlobalBest_Position, self.GlobalBest_Cost




