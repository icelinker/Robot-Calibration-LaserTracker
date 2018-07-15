function out = FARO_Take_Measure()
global FARO_DLL;

pxyz = calllib(FARO_DLL.libname, 'GetTarget', FARO_DLL.pint);
xyz = pxyz.value;
out = [xyz.x; xyz.y; xyz.z];

end
