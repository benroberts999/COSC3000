filename = 'data-csv-labels.dat';

data1 = readmatrix(filename);

% This autmatically skips all header lines
% But it doesn't know what to do with the comment line in the middle
% These lines are marked as 'NaN' in the matrix

length(data1)

% The rmmissing command deletes all the NaNs
data1 = rmmissing(data1);

length(data1)

% Alternatively, supply readmatrix with options
data2 = readmatrix(filename, "NumHeaderLines", 4, "Delimiter", ',', "CommentStyle",'#');
length(data2)

% Get x,y components
x = data2(:,1);
y = data2(:,2);

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


