# Adapte el RTree de Python para soportar los vectores característicos de Face Recognition en una
# búsqueda KNN con cola de prioridad.

from rtree import index
import face_recognition as fr
import os
import json
import heapq
import random

"""
Transforms a feature vector to an rtree point
for example:
input: (3, 4)
output: (3, 4, 3, 4)
"""
def generate_point(feature_vector):
    point = [0] * 2 * len(feature_vector)
    point[:len(feature_vector)] = feature_vector
    point[len(feature_vector):] = feature_vector
    return point

"""
initializes index property
"""
def initialize_index():
    p = index.Property()
    p.dimension = 128
    p.buffering_capacity = 4
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return p

"""
returns new clear index
"""
def get_clear_index():
    p = initialize_index()
    p.overwrite = True
    idx = index.Index('fr_index', properties=p)
    return idx

"""
returns index
"""
def get_index():
    p = initialize_index()
    p.overwrite = False
    idx = index.Index('fr_index', properties=p)
    return idx

"""
get face encodings from an image
"""
def get_face_encodings_from_image(image_path):
    image = fr.load_image_file(image_path)
    image_encoding = fr.face_encodings(image)
    return image_encoding

"""
generates index
"""
def generate_fr_index():
    idx = get_clear_index()
    image_names_idx = {}
    idx_counter = 0
    for image_name in os.listdir("images_short"):
        image_encoding = get_face_encodings_from_image("images_short/" + image_name)
        if image_encoding:
            feature_vector = image_encoding[0]
            feature_vector_as_point = generate_point(feature_vector)
            image_names_idx[idx_counter] = image_name
            idx.insert(idx_counter, feature_vector_as_point)
            idx_counter += 1
    with open("image_names_idx.json", "w") as images_json:
        json.dump(image_names_idx, images_json)

"""
distance between two images
"""
def distance_between_two_images(img1, img2):
    image1 = fr.load_image_file("images_short/" + img1)
    image2 = fr.load_image_file("images_short/" + img2)
    image1_encoding = fr.face_encodings(image1)
    image2_encoding = fr.face_encodings(image2)
    if not image1_encoding or not image2_encoding:
        return float("inf")
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    distance_between_images = fr.face_distance([image1_encoding], image2_encoding)
    return distance_between_images

"""
get k nearest neighbors from Q
"""
def knn_fr(q_image_name, k):
    query_image_encoding = get_face_encodings_from_image("images_short/" + q_image_name)
    neighbors = []
    images_names_idx = {}
    deleted_indeces = []
    idx = get_index()
    if query_image_encoding:
        with open("image_names_idx.json", "r") as images_json:
            images_names_idx = json.load(images_json)
        for i in range(k + 1):
            query_feature_vector = query_image_encoding[0]
            query_feature_vector_as_point = generate_point(query_feature_vector)
            nearest_neighbor = list(idx.nearest(coordinates=query_feature_vector_as_point, num_results=1))

            nearest_neighbor_encoding = get_face_encodings_from_image("images_short/" + images_names_idx[str(nearest_neighbor[0])])
            nearest_neighbor_feature_vector = nearest_neighbor_encoding[0]
            nearest_neighbor_feature_vector_as_point = generate_point(nearest_neighbor_feature_vector)

            deleted_indeces.append((nearest_neighbor[0], nearest_neighbor_feature_vector_as_point))
            idx.delete(nearest_neighbor[0], nearest_neighbor_feature_vector_as_point)
            if images_names_idx[str(nearest_neighbor[0])] != q_image_name:
                heapq.heappush(neighbors, (distance_between_two_images(q_image_name, images_names_idx[str(nearest_neighbor[0])]), nearest_neighbor[0]))
    neighbors_names = []
    for neighbor in neighbors:
        neighbors_names.append(images_names_idx[str(neighbor[1])])
    for deleted_index in deleted_indeces:
        idx.insert(deleted_index[0], deleted_index[1])
    return neighbors_names

generate_fr_index()
print(knn_fr("Zoran_Djindjic_0001.jpg", 3))
