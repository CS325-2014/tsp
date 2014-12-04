format long

file = 'result1.csv';
delim = ',';
headerlines = 1;

data = importdata(file, delim, headerlines);

headers = data.colheaders;

size = [];
processes = [];
time = [];

for i = 1:length(data.data)
    size(i) = data.data(i, 1);
    processes(i) = data.data(i, 2);
    time(i) = data.data(i, 3);
end

%[size, sortindex] = sort(size);
%size = size(sortindex);
%processes = processes(sortindex);
%time = time(sortindex);

scatter3(size, processes, time, 100, size, 'fill');

xlabel('# processes');
ylabel('max number');
zlabel('execution time (s)');
