struct temp{
	double temperature;
	double pressure;
	double humidity;
};
struct xyz{
	double x;
	double y;
	double z;
};

//// ONLY FOR DLL
extern "C" __declspec(dllexport) unsigned int CONNECT_AND_Initialise(char* ip, char* farofiles, char* faroexecutable, int PORT);
extern "C" __declspec(dllexport) int DISCONNECT_LAN(unsigned int pint);
///////////////////////////

//extern "C" __declspec(dllexport) int InitialiseTracker(char *ip, char *farofiles, char *faroexecutable, int PORT); //INIT
//extern "C" __declspec(dllexport) int FinaliseTracker(unsigned int pint);//FIN

extern "C" __declspec(dllexport) temp* Temperature(unsigned int pint);//TEMP
extern "C" __declspec(dllexport) int SetSamplesPerMeasure(unsigned int pint, int numsamples);//SAMPLES
extern "C" __declspec(dllexport) int SetSMRDiameter(unsigned int pint, double diameter);//DIAM
extern "C" __declspec(dllexport) int MeasureStorm(unsigned int pint, int samples, int measures);//STORM

extern "C" __declspec(dllexport) int FindTarget(unsigned int pint, xyz *pguess);//FIND
extern "C" __declspec(dllexport) int SMRPresent(unsigned int pint);//, xyz *pguess);//SMR
extern "C" __declspec(dllexport) int SetBackSide(unsigned int pint, int side);//BACK
extern "C" __declspec(dllexport) int Move_XYZ(unsigned int pint, xyz *pguess);//MOVE


extern "C" __declspec(dllexport) xyz* GetTarget(unsigned int pint);//GET


///////////////// WHATS INSIDE THE REAL APPLICATION:
/*
unsigned int InitialiseTracker(char *directory, char *ip); //INIT
int FinaliseTracker(unsigned int pint);//FIN

temp* Temperature(unsigned int pint);//TEMP
int SetSamplesPerMeasure(unsigned int pint, int numsamples);//SAMPLES
int SetSMRDiameter(unsigned int pint, double diameter);//DIAM
int MeasureStorm(unsigned int pint, int samples, int measures);//STORM

int FindTarget(unsigned int pint, xyz *pguess);//FIND
int SMRPresent(unsigned int pint);//, xyz *pguess);//SMR
int SetBackSide(unsigned int pint, int side);//BACK
int Move_XYZ(unsigned int pint, xyz *pguess);//MOVE

xyz* GetTarget(unsigned int pint, xyz *pxyzempty);//GET
*/
