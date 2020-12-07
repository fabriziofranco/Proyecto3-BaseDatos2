import heapq
import math
import json
import face_recognition
from rtree import index
import time

def generate_point(list):
    doble = []
    for i in list:
        doble.append(i)
    for i in list:
        doble.append(i)
    return tuple(i and i for i in doble)

def euclidean_distance(p1, p2):
    squared_dist = 0
    for i in range(len(p1)):
        squared_dist += math.pow(p1[i] - p2[i], 2)
    return math.sqrt(squared_dist)


def KNN_sequential(Q, k, path):
    total_path = 'data/' + path + '/'
    total_files = int(path)

    with open("diccionario_" + path + ".json") as json_file:
        dict = json.load(json_file)

    picture_1 = face_recognition.load_image_file(total_path + Q)
    face_encoding_1 = face_recognition.face_encodings(picture_1)
    if face_encoding_1:
        values = face_encoding_1[0].tolist()
        values = (generate_point(values))
        p = index.Property()
        p.dimension = 128  # D
        p.buffering_capacity = int(math.log(total_files, 10) ** 2) + 3 # M
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        p.overwrite = False
        idx = index.Index('face_recognition_index_' + path, properties=p)
        images = idx.intersection(idx.bounds, objects=True)
        neighbors = []
        for image in images:
            d = euclidean_distance(values, image.bbox)
            heapq.heappush(neighbors, (-d, image.id))
            if len(neighbors) > k:
                heapq.heappop(neighbors)
        neighbors = [(i, d * -1) for d, i in neighbors]
        neighbors.sort(key=lambda tup: tup[1])
        return [dict[str(i)] for i, d in neighbors]

print("Los dos vecinos mas cercano de auron1.jpg: ", KNN_sequential("auron1.jpg", 4, "400"))
