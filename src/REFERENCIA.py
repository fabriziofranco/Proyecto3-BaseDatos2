import face_recognition
from rtree import index
import os
import json

diccionario = {}


def duplicateandConvert(list):
    doble = []
    for i in list:
        doble.append(i)
    for i in list:
        doble.append(i)
    return tuple(i and i for i in doble)


def buildIndex():
    p = index.Property()
    p.dimension = 128  # D
    p.buffering_capacity = 4  # M
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx = index.Index('face_recognition_index', properties=p)

    contador = 0
    for filename in os.listdir("data"):
        picture_1 = face_recognition.load_image_file("data/" + filename)
        face_encoding_1 = face_recognition.face_encodings(picture_1)
        if face_encoding_1:
            values = face_encoding_1[0].tolist()
            values = (duplicateandConvert(values))
            diccionario.setdefault(len(diccionario),filename)
            idx.insert(len(diccionario)-1, values)

    file = open("diccionario.json", "w")
    json.dump(diccionario, file)
    file.close()


def KNN_FaceRecognition(Q, k):
    with open('diccionario.json') as json_file:
        dict = json.load(json_file)

    picture_1 = face_recognition.load_image_file("database_corta/" + Q)
    face_encoding_1 = face_recognition.face_encodings(picture_1)
    if face_encoding_1:
        values = face_encoding_1[0].tolist()
        values = (duplicateandConvert(values))
        p = index.Property()
        p.dimension = 128  # D
        p.buffering_capacity = 4  # M
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        p.overwrite=False
        idx = index.Index('face_recognition_index', properties=p)
        temp = list(idx.nearest(coordinates=values, num_results=k))
        vecinos = []
        for i in temp:
            vecinos.append(dict[str(i)])
    else:
        vecinos = []
    return vecinos

#buildIndex()
knn = KNN_FaceRecognition("Abdullah_0004.jpg", 4)
print("Los dos vecinos mas cercano de Abdullah_0004.jpg: ", knn)
