set terminal png
set datafile separator ","
set key autotitle columnhead
#unset key
set title 'Drone fl'
#set xlabel 'Time'
#set ylabel 'Percent Motor Speed'
set style fill solid 0.3
set style data lines
#motor velocities:
#plot 'drone_lateral.csv' using 1:4 with lines, '' using 1:8 with lines, '' using 1:6 with lines, '' using 1:10 with lines
#angles:
plot 'drone_lateral.csv' using 1:2 with lines, '' using 1:3 with lines