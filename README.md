# Proyecto3-BaseDatos2
Face recognition Web Platfrom

To do
- front end
- busqueda knn con cola de prioridad RTREE
- busqueda en rango RTREE
- busqueda knn con cola de prioridad secuencial
- busqueda en rango secuencial

| Tamaño (N)  | KNN R-Tree | KNN Sequential      |
| --- | ----------- |   ---    |
| 100 | 0.955 s |       |
| 200      | 0.966 s       |       |
| 400   | 0.986 s        |       |
| 800   | 1.008 s        |       |
| 1600   | 1.013 s        |       |
| 3200   | 0.962  s      |       |
| 6400   | 0.977 s        |       |
| 12800   | 1.068 s        |       |

Las consultas se ejecutaron 5 veces y se promedio el tiempo de respuesta para dar resultados más reales con un K=8. El capacity de los nodos se calcula de forma dinámica por la fórmula ```roun(log(total_files, 10) ** 2) + 3 ``` , lo cual permite que el índice siga siendo rápido, independientemente de la cantidad de elementos que se estima alojará, esto se evhaceidencia en buenos tiempos de respuesta para todos y cada uno de los índices construidos.
