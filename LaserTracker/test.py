import PyLaserTracker
import time 

LT=PyLaserTracker.API()
LT.Initialize()
LT.Move(100,20,30)
p=LT.Measure()
print(p[0])
LT.Finalize()