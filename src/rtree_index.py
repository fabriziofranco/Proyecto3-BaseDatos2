import face_recognition
from rtree import index
import os
import json
import math
import heapq

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

def KNN_FaceRecognition(Q, k, path):
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
        temp = list(idx.nearest(coordinates=values, num_results=k))
        vecinos = []
        for i in temp:
            vecinos.append(dict[str(i)])
    else:
        vecinos = []
    return vecinos


    


##rtree_index = Rtree_index("100")

rtree_index = Rtree_index("12800")

#knn = KNN_FaceRecognition("auron1.jpg", 4, "100")
#print("Los dos vecinos mas cercano de auron1.jpg: ", knn)

