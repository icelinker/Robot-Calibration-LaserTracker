function out = FARO_Finalise()
global FARO_DLL;
try
    unloadlibrary(FARO_DLL.libname);
catch e
end
out = 0;