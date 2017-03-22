set xlabel "Time(s)"
set ylabel "Tasks"
set terminal png
set output "imagem.png"
plot mrsg.out title "teste" with lines

#plot "map.out"  title "Map" with lines, "reduces.out"  title "Reduce" with lines
