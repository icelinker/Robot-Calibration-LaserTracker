function out = FARO_Weather_Conditions()

global FARO_DLL;

temp = calllib(FARO_DLL.libname, 'Temperature', FARO_DLL.pint);

val = temp.value;
val.humidity = val.humidity*100;

out = val;