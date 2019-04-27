set terminal png
set key autotitle columnhead
#set title 'PID Impulse Response'
#set xlabel 'Time'
#set ylabel 'Output'
#set style fill solid 0.3
set style data lines
plot 'pid_response.csv'