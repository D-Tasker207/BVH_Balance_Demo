from point import Point

class Ray:
    def __init__(self, origin: Point, direction: Point):
        if not isinstance(origin, Point):
            raise ValueError("origin must be a Point")
        
        if not isinstance(direction, Point):
            raise ValueError("direction must be a Point")
        _delta = 1e-6

        self._origin = origin + direction * _delta
        self._direction = direction

    def point_at(self, t: float) -> Point:
        return self.origin + self.direction * t
    
    def __str__(self):
        return "Ray({}, {})".format(self.origin, self.direction)
    
    def __repr__(self):
        return str(self)
    
    @property
    def origin(self) -> Point:
        return self._origin
    
    @property
    def direction(self) -> Point:
        return self._direction