# Proyecto 3: Face recognition Web Platfrom




## FrontEnd

### Búsqueda de vecinos cercanos
![Alt_text](https://i.ibb.co/b6GXx7y/Reconocimiento-KNN.gif)

### Búsqueda por rango
![Alt_text](https://i.ibb.co/ZMyGmRD/Reconocimiento-Rango.gif)

## Funcionamiento



<img src="https://i.ibb.co/zrjygDJ/Whats-App-Image-2020-12-07-at-12-06-11-PM.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="350" height="250" />


###### Fuente: Multimedia Database 2 - BASE DE DATOS 2- UTEC

La figura de arriba ilustra el funcionamiento de la base de Datos, las imágenes son representadas a partir de su vector característico y los índices son R-tree o secuencial. Apartir de las consultas sobre índice se accede a la base de datos y se retorna las imágenes correspondientes a la consulta.
### Construcción del índice

<img src="https://i.ibb.co/pJDv5p1/Whats-App-Image-2020-12-07-at-12-09-14-PM.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="300" height="300" />


###### Fuente: Multimedia Database 2 - BASE DE DATOS 2- UTEC

La creación del R-tree se da el constructor de la clase ```Rtree_index```, allí se inicializan todas las propiedades, la más importante es el capacity dada por la fórmula ```int(math.log(total_files, 10) ** 2) + 3```, esto dinamiza el índice y lo mantiene óptimo en inserciones y búsquedas. Este genera un archivo .index con el R-tree, un archivo .data con los ids de los elementos y sus vectores característicos y demás información de utilidad. Adicionalmente, genera un diccionario en json que guarda ID's con nombres de archivos. La estructura se crea vacía, pero para este proyecto se le insertan automáticamente los 100,200...,12800 elementos a cada índice R-tree correspondiente para la experimentación y pruebas.



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

Usamos la función `nearest` de la librería, y esta nos retorna directamente los K vecinos más cercanos.

Dicha función es recursiva. El caso base se da cuando se llega a un nodo hoja. Se itera a través de los nodos hijo del nodo hoja, y se van agregando a un max heap, de modo que si el heap se llena, simplemente se aplica un pop para eliminar el vecino más alejado. Cuando no se da el caso base, se itera a través de los hijos del nodo y se aplica MINDIST, para filtrar y evaluar si vale la pena seguir con la recursión por aquel nodo. En caso el nodo pase el filtro, se llama el mismo procedimiento recursivo sobre este.

#### Secuencial
    
Pasos:

1) Aprovechando los archivos `.data` generados por la librería del R-tree, usamos la función `intersect` para traer todos los resultados, pidiendo la intersección de los bounds máximos presentes en todo el árbol. Cabe recalcar que al hacer esto no estamos usando el índice R-tree, ya que vamos a iterar secuencialmente a través de todos las imágenes presentes en este índices.
2) Usamos un min heap para guardar los K vecinos más cercanos.
3) Luego, vamos cargando vecino a vecino (bloque a bloque).
    1) Calculamos la distancia euclideana entre el vecino actual y el query.
    2) Añadimos una tupla de la forma `(distancia * -1, id)` al min heap, para que este se comporte como un max heap.
    3) Si el tamaño del heap es mayor que K, hacemos pop al heap (borra el elemento máximo).
4) Una vez hayamos iterado secuencialmente a través de todos los vecinos, retornamos la respuesta.

### RANGE SEARCH

| Tamaño (N)  | Range Search R-Tree | Range Search Sequential      |
| --- | ----------- |   ---    |
| 100 |  0.82 s| 0.81 s |
| 200      | 0.766 s|  0.865 s     |
| 400   |0.801 s |   0.849 s    |
| 800   | 0.794 s | 0.964 s      |
| 1600   |0.806 s |  1.039 s    |
| 3200   |2.23 s |  2.015 s    |
| 6400   | 2.313 s|  2.032 s     |
| 12800   |2.339 s|  2.735 s     |

#### R-tree

Pasos:

1) Utilizar la función `generate_range_vector` para generar el vector que va a contener los rangos en los que se puede encontrar un vecino.
2) Usar la función `intersect` con el range vector generado, para que retorne las imágenes dentro de ese rango.
3) Ir cargando vecino a vecino (bloque a bloque), e ir agregándolo al resultado.
5) Retornar los resultados.

#### Secuencial
    
Pasos:

1) Aprovechando los archivos `.data` generados por la librería del R-tree, usamos la función `intersect` para traer todos los resultados, pidiendo la intersección de los bounds máximos presentes en todo el árbol. Cabe recalcar que al hacer esto no estamos usando el índice R-tree, ya que vamos a iterar secuencialmente a través de todos las imágenes presentes en este índices.
2) Luego, vamos cargando vecino a vecino (bloque a bloque).
3) Verificamos si el vecino se encuentra dentro del rango, y lo ingresamos al vector de respuesta.
4) Una vez hayamos iterado a través de todos los vecinos, retornamos la respuesta.



![Alt_text](https://i.ibb.co/Q6zGpBh/Whats-App-Image-2020-12-07-at-12-07-17-PM.jpg)
