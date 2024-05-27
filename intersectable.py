from ray import Ray
from point import Point
from abc import ABC, abstractmethod

class Intersectable(ABC):
    @property
    @abstractmethod
    def center(self) -> Point:
        pass

    @abstractmethod
    def intersect(self, ray: Ray) -> Point:
        pass