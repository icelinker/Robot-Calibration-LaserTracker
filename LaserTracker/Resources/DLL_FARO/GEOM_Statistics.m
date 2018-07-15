function [ output_args ] = GEOM_Statistics( meas , Title )
%GEOM_STATISTICS Summary of this function goes here
%   Detailed explanation goes here

figure;
subplot(1,3,1); plot([1:100],meas(1,:)); title([Title ' - X']);
subplot(1,3,2); plot([1:100],meas(2,:)); title([Title ' - Y']);
subplot(1,3,3); plot([1:100],meas(3,:)); title([Title ' - Z']);

fprintf(['Statistic for ' Title '\n']);
fprintf(' Std-3d : %f\n',sqrt(std(meas(1,:))^2+std(meas(2,:))^2+std(meas(3,:))^2));

fprintf('Axis X\n');
fprintf(' Mean : %f\n',mean(meas(1,:)));
fprintf(' Std  : %f\n',std(meas(1,:)));
fprintf(' Min  : %f\n',min(meas(1,:)));
fprintf(' Max  : %f\n',max(meas(1,:)));
fprintf(' Rng  : %f\n',max(meas(1,:))-min(meas(1,:)));

fprintf('Axis Y\n');
fprintf(' Mean : %f\n',mean(meas(2,:)));
fprintf(' Std  : %f\n',std(meas(2,:)));
fprintf(' Min  : %f\n',min(meas(2,:)));
fprintf(' Max  : %f\n',max(meas(2,:)));
fprintf(' Rng  : %f\n',max(meas(2,:))-min(meas(2,:)));

fprintf('Axis Z\n');
fprintf(' Mean : %f\n',mean(meas(3,:)));
fprintf(' Std  : %f\n',std(meas(3,:)));
fprintf(' Min  : %f\n',min(meas(3,:)));
fprintf(' Max  : %f\n',max(meas(3,:)));
fprintf(' Rng  : %f\n',max(meas(3,:))-min(meas(3,:)));
end

