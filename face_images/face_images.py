import train_config

from .impl import locally_images
from .impl import network_images

import face_recognition

from sklearn import svm

import pickle

def train():
    face_images_instance = locally_images.LocallyImages()
    if not train_config.get_property(section="IMAGES", option="IMAGES_LOCALLY"):
        face_images_instance = network_images.NetworkImages()

    people_faces = face_images_instance.get_people_faces()

    input_face_encodings = []
    output_face_encodings = []

    for p in people_faces:
        images = face_images_instance.get_images(p)
        for image in images:
            image_encoding = face_recognition.face_encodings(image)[0]
            input_face_encodings.append(image_encoding)
            output_face_encodings.append(p['id'])

    output_path = train_config.get_property("TRAIN", "OUTPUT_FILE_DIRECTORY")
    output_file_name = train_config.get_property("TRAIN", "OUTPUT_FILE_NAME")

    # clf = svm.SVC(gamma='scale')
    # clf.fit(input_face_encodings, output_face_encodings)

    face_encondings = {
        'input': input_face_encodings,
        'output': output_face_encodings,
        # 'clf': clf
    }

    with open(output_path + output_file_name, 'wb') as f:
        pickle.dump(face_encondings, f)