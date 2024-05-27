from intersectable import Intersectable
from point import Point
from ray import Ray
import math

class Circle(Intersectable):
    def __init__(self, center: Point, radius: int | float):
        if not isinstance(center, Point):
            raise ValueError("center must be a Point")
        
        if not isinstance(radius, (int, float)):
            raise ValueError("radius must be a number")
        
        self._radius = radius
        self._center = center

    def intersect(self, ray: Ray) -> Point:
        oc = ray.origin - self.center
        a = ray.direction.x ** 2 + ray.direction.y ** 2
        b = 2.0 * (oc.x * ray.direction.x + oc.y * ray.direction.y)
        c = oc.x ** 2 + oc.y ** 2 - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None, 1
        else:
            t1 = (-b - math.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2.0 * a)
            if t1 > 0:
                return ray.point_at(t1), 1
            elif t2 > 0:
                return ray.point_at(t2), 1
        return None, 1
    
    def __str__(self) -> str:
        return "Circle({}, {})".format(self.center, self.radius)
    
    @property
    def center(self) -> Point:
        return self._center
    
    @property
    def radius(self) -> float:
        return self._radius