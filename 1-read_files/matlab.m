data = readmatrix('data.dat');
%load data.dat % this also works for simple data

% Get x,y components
x = data(:,1);
y = data(:,2);

% Plot data
plot (x, y, 'r-', 'LineWidth', 2);
hold on 

% Simulate 25% error bars (just as example)
plot (x, 1.25*y, 'k--');
hold on 
plot (x, 0.75*y, 'k--');
hold off

title('Example: plot of function')
xlabel('variable (units)') 
ylabel('function (units)') 
legend({'function','error'})

% Save the plot as png
% 'gcf' = 'Get Current Figure'
saveas(gcf,'matlab.png')
