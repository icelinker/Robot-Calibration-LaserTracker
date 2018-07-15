function out = FARO_SMR_Present()

global FARO_DLL;

out = calllib(FARO_DLL.libname, 'SMRPresent', FARO_DLL.pint);
