# Proyecto3-BaseDatos2
Face recognition Web Platfrom



## FrontEnd

// Aqui va el front 


## Funcionamiento

### Construcción del índice


## Experimentación


### KNN SEARCH

| Tamaño (N)  | KNN R-Tree | KNN Sequential      |
| --- | ----------- |   ---    |
| 100 | 0.955 s | 0.811 s       |
| 200      | 0.966 s       |  0.833 s     |
| 400   | 0.986 s        |   0.858 s    |
| 800   | 1.008 s        | 0.97 s      |
| 1600   | 1.013 s        |  1.137 s    |
| 3200   | 0.962  s      |  1.488 s    |
| 6400   | 0.977 s        |  2.114 s     |
| 12800   | 1.068 s        |  3.569 s     |


Las consultas se ejecutaron 5 veces y se promedio el tiempo de respuesta para dar resultados más reales con un K=8. El capacity de los nodos se calcula de forma dinámica por la fórmula ```round(log(total_files, 10) ** 2) + 3 ``` , lo cual permite que el índice siga siendo rápido, independientemente de la cantidad de elementos que se estima alojará, esto se evidencia en buenos tiempos de respuesta para todos y cada uno de los índices construidos.


#### R-tree

Pasos:

1) Utilizar la función `generate_range_vector` para generar el vector que va a contener los rangos en los que se puede encontrar un vecino.
2) Utilizar la función `nearest` de la librería, para obtener los vecinos más cercanos en orden.
3) Ir cargando vecino a vecino (bloque a bloque). (MIN-DIST)
4) Verificar si el vecino se encuentra dentro del vector de rangos usando la función `is_inside_range`.
    1) Si se encuentra dentro, se añade a los resultados.
    2) En caso contrario, dejamos de iterar los vecinos, dado que como han sido retornados en orden, si este vecino no se encuentra dentro de rango, quiere decir que los vecinos restantes tampoco lo están.
5) Retornar los resultados.

#### Secuencial
    
Pasos:

1) Aprovechando los archivos `.data` generados por la librería del R-tree, usamos la función `intersect` para traer todos los resultados, pidiendo la intersección de los bounds máximos presentes en todo el árbol. Cabe recalcar que al hacer esto no estamos usando el índice R-tree, ya que vamos a iterar secuencialmente a través de todos las imágenes presentes en este índicea
2) Luego, vamos cargando vecino a vecino (bloque a bloque).
3) Verificamos si el vecino se encuentra dentro del rango, y lo ingresamos al vector de respuesta.
4) Una vez hayamos iterado a través de todos los vecinos, retornamos la respuesta.



#### R-tree
#### Secuencial

### RANGE SEARCH

| Tamaño (N)  | Range Search R-Tree | Range Search Sequential      |
| --- | ----------- |   ---    |
| 100 |  0.892 s| 0.81 s |
| 200      | 0.849 s|  0.865 s     |
| 400   |0.964 s |   0.849 s    |
| 800   | 1.062 s | 0.964 s      |
| 1600   |1.154 s |  1.039 s    |
| 3200   |1.360 s |  2.015 s    |
| 6400   | 1.444 s|  2.032 s     |
| 12800   |1.945 s|  2.735 s     |

#### R-tree

Pasos:

1) Utilizar la función `generate_range_vector` para generar el vector que va a contener los rangos en los que se puede encontrar un vecino.
2) Utilizar la función `nearest` de la librería, para obtener los vecinos más cercanos en orden.
3) Ir cargando vecino a vecino (bloque a bloque). (MIN-DIST)
4) Verificar si el vecino se encuentra dentro del vector de rangos usando la función `is_inside_range`.
    1) Si se encuentra dentro, se añade a los resultados.
    2) En caso contrario, dejamos de iterar los vecinos, dado que como han sido retornados en orden, si este vecino no se encuentra dentro de rango, quiere decir que los vecinos restantes tampoco lo están.
5) Retornar los resultados.

#### Secuencial
    
Pasos:

1) Aprovechando los archivos `.data` generados por la librería del R-tree, usamos la función `intersect` para traer todos los resultados, pidiendo la intersección de los bounds máximos presentes en todo el árbol. Cabe recalcar que al hacer esto no estamos usando el índice R-tree, ya que vamos a iterar secuencialmente a través de todos las imágenes presentes en este índicea
2) Luego, vamos cargando vecino a vecino (bloque a bloque).
3) Verificamos si el vecino se encuentra dentro del rango, y lo ingresamos al vector de respuesta.
4) Una vez hayamos iterado a través de todos los vecinos, retornamos la respuesta.
