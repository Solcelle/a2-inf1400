import math
import random

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
             return Vector2(self.x + other[0], self.y + other[1])
        return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, tuple):
             return Vector2(self.x - other[0], self.y - other[1])
        return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2(self.x / other.x, self.y / other.y)
        return Vector2(self.x / other, self.y / other)

def length_sqr(vec):
    return vec.x ** 2 + vec.y ** 2

def length(vec):
    return math.sqrt(length_sqr(vec))


# Returns vector normalized
def normalize(vec):
    vec_length = length(vec)

    if vec_length < 0.00001:
        return Vector2(0.00001, 0.00001)

    return Vector2(vec.x / vec_length, vec.y / vec_length)

# Returns distance between two vectors
def dist(vec1, vec2):
    return length(vec1 - vec2)

# Returns direction from one vector to another
def direction_to(vec1, vec2):
    radians = math.atan2(vec2.y - vec1.y, vec2.x - vec1.x)
    return (math.cos(radians), math.sin(radians))

# Returns a random vector
def random_vector():
    return Vector2(random.random() * 2.0 - 1.0, random.random() * 2.0 - 1.0)