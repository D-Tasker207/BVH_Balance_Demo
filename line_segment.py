from intersectable import Intersectable
from point import Point
from ray import Ray

class LineSegment(Intersectable):
    def __init__(self, start: Point, end: Point):
        if not isinstance(start, Point):
            raise ValueError("start must be a Point")
        
        if not isinstance(end, Point):
            raise ValueError("end must be a Point")
        
        self._start = start
        self._end = end

    def intersect(self, ray: Ray) -> Point:
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        x3, y3 = ray.origin.x, ray.origin.y
        x4, y4 = ray.origin.x + ray.direction.x, ray.origin.y + ray.direction.y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None, 1   # Parallel lines

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        if 0 <= t <= 1 and u >= 0:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return Point(intersection_x, intersection_y), 1
        return None, 1
    
    def __str__(self) -> str:
        return "LineSegment({}, {})".format(self.start, self.end)

    @property
    def start(self) -> Point:
        return self._start
    
    @property
    def end(self) -> Point:
        return self._end
    
    @property
    def center(self) -> Point:
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)