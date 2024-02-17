#!/usr/bin/env gnuplot
set term wxt persist

# See:
# https://gnuplotting.org/output-terminals/index.html
# for terminal (font/style etc.) options

set title 'Example: plot of function'
set xlabel 'variable (units)'
set ylabel 'function (units)'

set border linewidth 2

set xrange [0:6.62]

# Change data file delimeter like this
set datafile separator ","

# That's all we have to do - gnuplot will simply ignore lines it
# doesn't undertand

# plot "data-csv-labels.dat" using 1:2 skip 3 with lines linecolor 'red' linewidth 2 title, \
#   "" u 1:($2*0.75) w l dt 2 lc 'black' lw 2 t "error",\
#   "" u 1:($2*1.25) w l dt 2 lc 'black' lw 2 notitle

# But, if we want to use the columntitles, we can tell it to skip first three:
plot "data-csv-labels.dat" using 1:2 skip 3 with lines linecolor 'red' linewidth 2 title columnheader(2), \
  "" u 1:($2*0.75) w l dt 2 lc 'black' lw 2 t "error",\
  "" u 1:($2*1.25) w l dt 2 lc 'black' lw 2 notitle