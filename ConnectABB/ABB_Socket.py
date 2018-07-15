import socket
import sys
import select
import struct

class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

        print("connected")

    def sendFloats(self, FloatsList):
        MSGLEN = len(FloatsList)
        totalsent = 0
        while totalsent < MSGLEN:
            msg=bytes(list(struct.pack('f',FloatsList[totalsent]))[::-1])
            sent = self.sock.send(msg)
            if sent < 4:
                raise RuntimeError("socket connection broken")
            else:
                totalsent = totalsent + 1

    def sendInts(self, IntsList):
        MSGLEN = len(IntsList)
        totalsent = 0
        while totalsent < MSGLEN:
            msg=bytes(list(struct.pack('i',IntsList[totalsent]))[::-1])
            sent = self.sock.send(msg)
            if sent < 4:
                raise RuntimeError("socket connection broken")
            else:
                totalsent = totalsent + 1

    def sendOneByte(self, msg):
        MSGLEN=1
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg.to_bytes(1,sys.byteorder))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receiveFloats(self,MSGLEN):
        self.sock.setblocking(1)
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN*4:
            chunk = self.sock.recv(min(MSGLEN*4 - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        raw=chunks[0]
        inv_raw = list(raw)
        b = bytes(inv_raw[::-1])
        format='f'
        for i in range(1,MSGLEN):
            format=format+' f'
        SS = struct.unpack(format, b)
        Floats = SS[::-1]
        return Floats

    def receiveOneByte(self):
        self.sock.setblocking(1)
        chunks = []
        bytes_recd = 0
        MSGLEN = 1
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        raw=chunks[0]
        return int.from_bytes(raw,sys.byteorder)
    def closeConnection(self):
        self.sock.close()

class ABB_Socket:
    def __init__ (self, controllerIP, port):
        self.s=mysocket()
        self.s.connect(controllerIP, port)


    def ReadJoints(self):
        '''
        ReadJoints reads the current joints angles of the robot.
        Returns joints values in degrees in a 6X1 vector.

        :return:
        '''
        actioncode = 1  #signal telling the server you want the joint
        #angles
        self.s.sendOneByte(actioncode)
        J=self.s.receiveFloats(6)

        return J

    def MoveAbsJ (self, joints):
        '''
        Move the robot the specified joints values in degrees.
        Returns a signal (1) when the movement is complete.

        :param joints:
        :return:
        '''
        actioncode = 2    #signal telling the server you want to move
                            #the robot
        self.s.sendOneByte(actioncode)
        self.s.sendFloats(joints)

        #the return signal telling the movement is completed
        signal = self.s.receiveOneByte()
        return signal

    def SetTCPSpeed (self, speed):
        '''
        Set the TCP speed of the robot in mm/s

        :param speed:
        :return:
        '''
        actioncode = 3    #signal telling the server you want to set
                            #the TCP speed.
        self.s.sendOneByte(actioncode)
        self.s.sendInts([speed])

    def delete(self):
        '''
        Close and delete the TCPIP connection

        :return:
        '''
        self.s.closeConnection()
        print("socket deleted")


"""
    def MoveAbsJNoWait (self, joints):
        '''
        Move the robot the specified joints values in degrees.
        MATLAB doesnt wait for the movement to be completed.

        :param joints:
        :return:
        '''
        actioncode = 4     #signal telling the server you want to move
        self.s.sendOneByte(actioncode)
        self.s.sendFloats(joints)
        signal = self.s.receiveOneByte()
        return signal
"""


