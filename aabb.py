from intersectable import Intersectable
import matplotlib.pyplot as plt
import random
from point import Point
from ray import Ray

class AABB(Intersectable):
    def __init__(self, min: Point, max: Point):
        if not isinstance(min, Point):
            raise ValueError("min must be a Point")
        if not isinstance(max, Point):
            raise ValueError("max must be a Point")
        
        self._min = min
        self._max = max

    def intersect(self, ray: Ray) -> tuple[bool, int]:
        tmin, tmax = float('-inf'), float('inf')
        tymin, tymax = float('-inf'), float('inf')

        if(ray.direction.x != 0):
            tmin = (self.min.x - ray.origin.x) / ray.direction.x
            tmax = (self.max.x - ray.origin.x) / ray.direction.x
        if tmin > tmax:
            tmin, tmax = tmax, tmin

        if(ray.direction.y != 0):
            tymin = (self.min.y - ray.origin.y) / ray.direction.y
            tymax = (self.max.y - ray.origin.y) / ray.direction.y
        if tymin > tymax:
            tymin, tymax = tymax, tymin

        if (tmin > tymax) or (tymin > tmax):
            return False, 1

        tmin = max(tmin, tymin)
        tmax = min(tmax, tymax)

        return tmax > max(tmin, 0), 1
    
    def union(self, other: 'AABB') -> 'AABB':
        if not isinstance(other, AABB):
            raise ValueError("Union not supported between AABB and {}".format(type(other)))
        
        return AABB(Point(min(self.min.x, other.min.x), min(self.min.y, other.min.y)),
                    Point(max(self.max.x, other.max.x), max(self.max.y, other.max.y)))
    
    def plot(self, ax, alpha=0.3, color='green'):
        rect = plt.Rectangle((self.min.x, self.min.y), 
                             self.max.x - self.min.x, 
                             self.max.y - self.min.y, 
                             linewidth=1, edgecolor=color, facecolor=color, alpha=alpha)
        ax.add_patch(rect)
    
    @property
    def center(self) -> Point:
        return Point((self.min.x + self.max.x) / 2, (self.min.y + self.max.y) / 2)
    
    @property
    def max(self) -> Point:
        return self._max
    
    @property
    def min(self) -> Point:
        return self._min