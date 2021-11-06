import abc
from abc import ABC, abstractmethod

class FaceImages(ABC):
    @abstractmethod
    def get_people_faces():
        pass

    @abstractmethod
    def get_images(person):
        pass