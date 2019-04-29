set terminal png
set datafile separator ","
set key autotitle columnhead
#unset key
set title 'Drone fl'
#set xlabel 'Time'
#set ylabel 'Percent Motor Speed'
set style fill solid 0.3
set style data lines
plot 'drone_position.csv' using 1:4 with lines, '' using 1:8 with lines