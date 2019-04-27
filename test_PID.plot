set terminal png
set datafile separator ","
set key autotitle columnhead
unset key
set title 'PID Impulse Response'
set xlabel 'Time'
set ylabel 'Speed'
set style fill solid 0.3
set style data lines
plot 'pid_response.csv'