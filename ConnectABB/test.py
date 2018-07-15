from ABB_Socket import ABB_Socket
from time import sleep

connection = ABB_Socket("192.168.125.1", 1025)


connection.SetTCPSpeed(100)
s=connection.MoveAbsJ([0, 0, 0, 0, 0, 0])
print(connection.ReadJoints())
s=connection.MoveAbsJ([30, 0, 0, 0, 0, 0])
print(connection.ReadJoints())
s=connection.MoveAbsJ([-30, 0, 0, 0, 0, 0])
print(connection.ReadJoints())

connection.delete()




