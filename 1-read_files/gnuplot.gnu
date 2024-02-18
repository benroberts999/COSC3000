#!/usr/bin/env gnuplot
set term wxt persist

# To save directly to png, replace above with:
# There are many really nice terminals, particularly cairolatex

# set term pngcairo
# set output "gnuplot.png"

# See:
# https://gnuplotting.org/output-terminals/index.html
# for terminal (font/style etc.) options

set title 'Example: plot of function'
set xlabel 'variable (units)'
set ylabel 'function (units)'

set border linewidth 2

set xrange [0:6.62]

plot "data.dat" using 1:2 with lines linecolor 'red' linewidth 2 title "function", \
  "" u 1:($2*0.75) w l dt 2 lc 'black' lw 2 t "error",\
  "" u 1:($2*1.25) w l dt 2 lc 'black' lw 2 notitle

# Don't need to repeat filename for second plot command
# note use of short-hand in second two rows
# the '\' character is required to continue reading from new line