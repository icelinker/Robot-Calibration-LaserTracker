function out = FARO_Initialise()
global FARO_DLL;
notify = 1;
FARO_DLL.libname = 'DLL_FARO';

FARO_DLL.FARO_DIR = [pwd, '\DLL_FARO\'];
FARO_DLL.FARO_FILES_DIR = ['C:/FARO/LT/'];
FARO_DLL.IP = '192.168.125.2';
FARO_DLL.PORT = 3500;
SYSTEM_EXEC_CMD = ['"cmd /c start C:/FARO/EXE_FARO/EXE_FARO.exe - ', int2str(FARO_DLL.PORT),'"'];

try
    try
        unloadlibrary(FARO_DLL.libname);
%         unloadlibrary('DLL_FARO');
    catch E
    end
    loadlibrary([FARO_DLL.FARO_DIR, 'DLL_FARO\DLL_FARO.dll'], [FARO_DLL.FARO_DIR, 'DLL_FARO\DLL_FARO.h']);
    FARO_DLL.pint = calllib(FARO_DLL.libname, 'CONNECT_AND_Initialise', FARO_DLL.IP, FARO_DLL.FARO_FILES_DIR, SYSTEM_EXEC_CMD, FARO_DLL.PORT);
catch E
    if notify
        msgbox(E.message,'Error while connecting to library');
    end
    FARO_DLL.pint = 0;
end
       
if FARO_DLL.pint == 0
    error('problems when calling library');
end

out = FARO_DLL;

return













% v = [4 6 8; 7 5 3];

% pv = libpointer('int16Ptr', v);
% get(pv, 'Value')
% % ans =
% %      4     6     8
% %      7     5     3
% % Now call the C function in the library, passing the pointer to v. If you were to pass a copy of v, the results would be lost once the function terminates. Passing a pointer to v enables you to get back the results:
% 
% calllib('shrlibsample', 'multiplyShort', pv, 6);
% get(pv, 'Value')
% % ans =
% %      0    12    32
% %      7    15    15









