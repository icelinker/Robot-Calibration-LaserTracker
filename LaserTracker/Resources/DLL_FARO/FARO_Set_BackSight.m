function out = FARO_Set_BackSight()

global FARO_DLL;

out = calllib(FARO_DLL.libname, 'SetBackSide', FARO_DLL.pint, 1);
