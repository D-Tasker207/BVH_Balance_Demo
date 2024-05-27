class Point:
    def __init__(self, x: int | float, y: int | float):
        if not isinstance(x, (int, float)):
            raise ValueError("x must be a number")
        if not isinstance(y, (int, float)):
            raise ValueError("y must be a number")
        
        self._x = x
        self._y = y
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        else:
            raise ValueError("Multiplication not supported between Point and {}".format(type(other)))    
        
    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        return str(self)
    
    @property
    def x(self) -> int | float:
        return self._x
    
    @property
    def y(self) -> int | float:
        return self._y