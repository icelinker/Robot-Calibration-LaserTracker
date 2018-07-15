function out = FARO_Search_SMR(xyz)

global FARO_DLL;

pxyz.x = xyz(1);
pxyz.y = xyz(2);
pxyz.z = xyz(3);

out = calllib(FARO_DLL.libname, 'FindTarget', FARO_DLL.pint, pxyz);
