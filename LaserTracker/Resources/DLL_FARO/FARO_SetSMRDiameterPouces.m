function out = FARO_SetSMRDiameterPouces(diameter)

global FARO_DLL;

out = calllib(FARO_DLL.libname, 'SetSMRDiameter', FARO_DLL.pint, diameter);