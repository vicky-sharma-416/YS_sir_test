#!/usr/bin/python
# -*- coding: utf-8 -*-

import face_recognition


def identifyface(image_path):
    my_dir = './source/'  # Folder where all your image files reside. Ensure it ends with
    encoding_for_file = []  # Create an empty list for saving encoded files
    for i in os.listdir(my_dir):  # Loop over the folder to list individual files
        image = my_dir + i
        image = face_recognition.load_image_file(image)  # Run your load command
        image_encoding = face_recognition.face_encodings(image)  # Run your encoding command
        encoding_for_file.append(image_encoding[0])  # Append the results to encoding_for_file list
    results = face_recognition.compare_faces(encoding_for_file,
            image_path)
    return results
