from aabb import AABB
from circle import Circle
from line_segment import LineSegment
from point import Point
from ray import Ray
from intersectable import Intersectable


class BVHNode:
    def __init__(self, objects: list[Intersectable], use_midpoint: bool = False):
        if len(objects) == 1:
            self.left = self.right = objects[0]
            self.aabb = self.calculate_aabb(objects[0])
        elif len(objects) == 2:
            self.left = objects[0]
            self.right = objects[1]
            self.aabb = self.calculate_aabb(objects[0]).union(self.calculate_aabb(objects[1]))
        else:
            # Determine the axis with the largest range
            min_x = min(obj.center.x for obj in objects)
            max_x = max(obj.center.x for obj in objects)
            min_y = min(obj.center.y for obj in objects)
            max_y = max(obj.center.y for obj in objects)

            range_x = max_x - min_x
            range_y = max_y - min_y

            if range_x > range_y:
                objects.sort(key=lambda obj: obj.center.x)
            else:
                objects.sort(key=lambda obj: obj.center.y)

            if(use_midpoint):
                # Split the objects in half
                best_split = len(objects) // 2
            else:
                # Find the best split point to minimize the midpoint distance
                best_split = None
                best_midpoint_distance = float('-inf')
                for i in range(1, len(objects)):
                    left = objects[:i]
                    right = objects[i:]
                    left_center = sum(obj.center.x for obj in left) / len(left) if range_x > range_y else sum(obj.center.y for obj in left) / len(left)
                    right_center = sum(obj.center.x for obj in right) / len(right) if range_x > range_y else sum(obj.center.y for obj in right) / len(right)
                    midpoint_distance = abs(left_center - right_center)
                    if midpoint_distance > best_midpoint_distance:
                        best_midpoint_distance = midpoint_distance
                        best_split = i

            self.left = BVHNode(objects[:best_split])
            self.right = BVHNode(objects[best_split:])
            self.aabb = self.left.aabb.union(self.right.aabb)

    def calculate_aabb(self, obj: Intersectable) -> AABB:
        if isinstance(obj, LineSegment):
            min_point = Point(min(obj.start.x, obj.end.x), min(obj.start.y, obj.end.y))
            max_point = Point(max(obj.start.x, obj.end.x), max(obj.start.y, obj.end.y))
        elif isinstance(obj, Circle):
            min_point = Point(obj.center.x - obj.radius, obj.center.y - obj.radius)
            max_point = Point(obj.center.x + obj.radius, obj.center.y + obj.radius)
        return AABB(min_point, max_point)

    def intersect(self, ray: Ray) -> tuple[Point, int]:
        if not self.aabb.intersect(ray)[0]:
            return None, 1

        hit_left, l_intersect_calls = self.left.intersect(ray)
        hit_right, r_intersect_calls = self.right.intersect(ray)

        if hit_left and hit_right:
            dist_left = (hit_left - ray.origin).x ** 2 + (hit_left - ray.origin).y ** 2
            dist_right = (hit_right - ray.origin).x ** 2 + (hit_right - ray.origin).y ** 2
            return hit_left if dist_left < dist_right else hit_right, l_intersect_calls + r_intersect_calls + 1
        elif hit_left:
            return hit_left, l_intersect_calls + r_intersect_calls + 1
        elif hit_right:
            return hit_right, l_intersect_calls + r_intersect_calls + 1
        else:
            return None, l_intersect_calls + r_intersect_calls + 1
        
    def printTree(self):
        def printTreeHelper(node, level, nodeid=[0]):
            if isinstance(node, BVHNode):
                print(" " * level + "Node{}".format(nodeid[0]))
                nodeid[0] += 1
                printTreeHelper(node.left, level + 1, nodeid)
                printTreeHelper(node.right, level + 1, nodeid)
            else:
                print(" " * level + str(node))
        
        printTreeHelper(self, 0)