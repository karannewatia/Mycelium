set terminal pdf color size 10.4cm,3.8cm font "Helvetica, 7"
set output "../new_graphs/User_bandwidth.pdf"
set border 15
set grid
set size 1.0, 1.0
set style fill solid 1.00 border -1
set datafile missing '-'
set boxwidth 0.3 absolute
set key top right rmargin
set lmargin 13
set bmargin 7
set tmargin 2
set xlabel "Number of hops in the communication path"
set xlabel offset 0, -0.5, 0
set ylabel "Traffic (MB sent)" offset -6
set xtics font "Helvetica, 12"
set xtics nomirror ("2" 0, "3" 1.5, "4" 3, "2" 4.5, "3" 6, "4" 7.5)
set ytics font "Helvetica, 14"
set xlabel font "Helvetica, 14"
set ylabel font "Helvetica, 14"
set key font "Helvetica, 14"
set xtics nomirror
set ytics nomirror ("1" 1, "10" 10, "10^2" 100, "10^3" 1000, "10^4" 10000)
set logscale y
set ytics logscale
plot [-1:8][1:10000] \
"bw-user.data" using ($1-0.3):($2) lt 2 lw 3 pt 2 ps 0.7 lc rgb "green" with boxes title "r=1, non-forwarder",\
"bw-user.data" using ($1):($3) lt 1 lw 3 pt 1 ps 0.7 lc rgb "orange" with boxes  title "r=2, non-forwarder",\
"bw-user.data" using ($1+0.3):($4) lt 1 lw 3 pt 1 ps 0.7 lc rgb "blue" with boxes  title "r=3, non-forwarder",\
"bw-user.data" using ($5-0.3):($6) lt 2 lw 3 pt 2 ps 0.7 lc rgb "purple" with boxes title "r=1, forwarder",\
"bw-user.data" using ($5):($7) lt 1 lw 3 pt 1 ps 0.7 lc rgb "pink" with boxes title "r=2, forwarder",\
"bw-user.data" using ($5+0.3):($8) lt 1 lw 3 pt 1 ps 0.7 lc rgb "red" with boxes title "r=3, forwarder",\
