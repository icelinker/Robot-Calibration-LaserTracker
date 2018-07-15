function out = FARO_Move_XYZ(xyz)

global FARO_DLL;

pxyz.x = xyz(1);
pxyz.y = xyz(2);
pxyz.z = xyz(3);

out = calllib(FARO_DLL.libname, 'Move_XYZ', FARO_DLL.pint, pxyz);

