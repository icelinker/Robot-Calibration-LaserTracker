function out = FARO_SetSamplesPerMeasure(num)

global FARO_DLL;

out = calllib(FARO_DLL.libname, 'SetSamplesPerMeasure', FARO_DLL.pint, round(num));