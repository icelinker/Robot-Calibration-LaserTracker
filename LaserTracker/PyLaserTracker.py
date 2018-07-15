from ctypes import *
import os

class point(Structure):
	_fields_ = [("x", c_double),
                ("y", c_double),
				("z", c_double)]

class API:
	def __init__(self):
		self.FARO_FILES_DIR = 'C:/FARO/LT/'
		self.IP = '192.168.0.2'
		self.PORT = 3500
		self.SYSTEM_EXEC_CMD = 'cmd /c start C:/FARO/EXE_FARO/EXE_FARO.exe - 3500'
		self.DLL_file="C:/FARO/FARO_DLL/DLL_FARO.dll"

	def Initialize(self):
		if os.path.isfile(self.DLL_file):
			self.FARODLL=cdll.LoadLibrary(self.DLL_file)
			self.FARODLL.GetTarget.restype=POINTER(point)
			self.FARODLL.FindTarget.restype=POINTER(point)
			self.FARODLL.CONNECT_AND_Initialise.restype=c_uint
			self.connection = self.FARODLL.CONNECT_AND_Initialise(c_char_p(self.IP.encode('utf-8')), c_char_p(self.FARO_FILES_DIR.encode('utf-8')), c_char_p(self.SYSTEM_EXEC_CMD.encode('utf-8')), 3500)
		else:
			print("cannot find the file: C:/FARO/FARO_DLL/DLL_FARO.dll")

	def Move(self,x,y,z):
		p = point(x,y,z)
		self.FARODLL.Move_XYZ(self.connection,byref(p))
		
	def Find(self,x,y,z):
		p1 = point(x,y,z)
		p2 = self.FARODLL.FindTarget(self.connection,byref(p1))
		if self.SMRpresent():
			return self.Measure()
		else:
			return [0, 0, 0]

		
	def SMRpresent(self):
		return self.FARODLL.SMRPresent(self.connection)
		
	def Measure(self):
		p = self.FARODLL.GetTarget(self.connection)
		return [p.contents.x, p.contents.y, p.contents.z]
		
	def SetSamples(self,n):
		self.FARODLL.SetSamplesPerMeasure(self.connection,c_int(n))

	def SetSMRDiameterPouces(self,diameter):
		self.FARODLL.SetSMRDiameter(self.connection,c_double(diameter))
		
	def Finalize(self):
		print(self.FARODLL.DISCONNECT_LAN(self.connection))
		os.system("TASKKILL /F /IM EXE_FARO.exe")
