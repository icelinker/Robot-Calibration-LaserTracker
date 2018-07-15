%%=========================================================================
%|  CALIBRATION CODE V2.0                                                 |
%|  ALEXANDRE FILION - ETS/CORO (2014)                                    |
%|                                                                        |
%%=========================================================================
function [Output, Result] = FARO_SearchAt(XYZ)
    Result = FARO_Search_SMR(XYZ);
    if Result == 0
        fprintf('Not found.\n');
        Output = [0,0,0];
    elseif Result == 1
        fprintf('Found with bad orientation.\n');
        Output = [1,1,1];
    elseif Result == 2
        fprintf('Found.\n');
        Output = transpose(FARO_Take_Measure());
    end
end