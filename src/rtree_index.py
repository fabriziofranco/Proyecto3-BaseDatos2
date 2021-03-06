import face_recognition
from rtree import index
import os
import json
import math
import heapq
import time

diccionario = {}

class Rtree_index:

    def __init__(self, path):
        total_files = int(path)
        total_path = 'data/' + path + '/'

        p = index.Property()
        p.dimension = 128  # D
        p.buffering_capacity = int(math.log(total_files, 10) ** 2) + 3 # M
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        idx = index.Index('face_recognition_index_' + path, properties=p)

        self.total_files = total_files
        self.path = path
        self.total_path = total_path

        for filename in os.listdir(total_path):
            picture_1 = face_recognition.load_image_file(total_path + filename)
            face_encoding_1 = face_recognition.face_encodings(picture_1)
            if face_encoding_1:
                values = face_encoding_1[0].tolist()
                values = (generate_point(values))
                diccionario.setdefault(len(diccionario), filename)
                idx.insert(len(diccionario) - 1, values)

        file = open("diccionario_" + path + ".json", "w")
        json.dump(diccionario, file)
        file.close()

def init_search(Q, path,frontEnd):
    if frontEnd==False:
        total_path = 'data/' + path + '/'
    else:
        total_path = 'data/imageInput/'
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
        return idx, values, dict
    else:
        return None,None,None

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

def KNN_FaceRecognition(Q, k, path,frontEnd=True):
    idx, feature_vector, names_dict = init_search(Q, path,frontEnd)
    if idx == None:
        return []
    temp_vecinos = list(idx.nearest(coordinates=feature_vector, num_results=k))
    vecinos = []
    for i in temp_vecinos:
        vecinos.append(names_dict[str(i)])
    return vecinos


#######################################

def generate_range_vector(feature_vector, r):
    range_vector = [0] * len(feature_vector)
    for i in range(len(feature_vector) // 2):
        range_vector[i] = feature_vector[i] - r
        range_vector[i + len(feature_vector) // 2] = feature_vector[i] + r
    return range_vector

def range_search_rtree(Q, r, path,frontEnd):
    idx, feature_vector, names_dict = init_search(Q, path,frontEnd)
    result = []
    range_vector = generate_range_vector(feature_vector, r)
    temp_vecinos = idx.intersection(range_vector, objects=True)
    cont = 0
    for vecino in temp_vecinos:
        result.append(names_dict[str(vecino.id)])
    return result

#######################################

# rtree_index  = Rtree_index("100")
# rtree_index2 = Rtree_index("200")
# rtree_index3 = Rtree_index("400")
# rtree_index4 = Rtree_index("800")
# rtree_index5 = Rtree_index("1600")
# rtree_index6 = Rtree_index("3200")
# rtree_index7 = Rtree_index("6400")
# rtree_index8 = Rtree_index("12800")

### Experimientos 

# start = time.time()
# print("\nRange search - Vecinos de auron: ", range_search_rtree("auron1.jpg", 0.15, "12800", False))
# print(time.time() - start)
#print(knn)
