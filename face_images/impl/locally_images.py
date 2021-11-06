import json
import numpy as np
import PIL

import util
import face_images.FaceImages
import train_config

class LocallyImages(face_images.FaceImages.FaceImages):
    def __init__(self):
        self.rootPath = util.get_project_root()
        self.imagesFolder = self.rootPath.joinpath(train_config.get_property('IMAGES', 'LOAD_IMAGES_FOLDER'))
    
    def get_people_faces(self):
        people_data = self.rootPath.joinpath('assets', 'data', 'people_data.json').read_text(encoding="UTF-8")
        return json.loads(people_data)

    def get_images(self, person):
        
        images = []

        for image in self.imagesFolder.joinpath(str(person['id'])).iterdir():
            im = PIL.Image.open(image).convert('RGB')
            images.append(np.array(im))
    #         im = PIL.Image.open(file)
    # if mode:
    #     im = im.convert(mode)
    # return np.array(im)
    #         face_recognition.load_image_file
        return images