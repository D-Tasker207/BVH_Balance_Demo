import numpy as np
import matplotlib.pyplot as plt
import random
from intersectable import Intersectable
from point import Point
from ray import Ray
from circle import Circle
from line_segment import LineSegment
from bvh_node import BVHNode

USE_MIDPOINT = True

def cast_rays(light_source: Point, bvh: BVHNode, num_rays: int = 360) -> tuple[list[Ray], list[Point]]:
    rays = []
    intersections = []
    total_intersect_calls = 0
    for angle in np.linspace(0, 2 * np.pi, num_rays):
        direction = Point(np.cos(angle), np.sin(angle))
        ray = Ray(light_source, direction)
        rays.append(ray)
        intersection, num_intersect_calls = bvh.intersect(ray)
        if intersection:
            intersections.append(intersection)
        total_intersect_calls += num_intersect_calls
    return rays, intersections, total_intersect_calls, total_intersect_calls / num_rays

def plot_scenes(scenes: list[dict[Point, list[Point], list[Intersectable], BVHNode]]) -> None:
    fig, ax = plt.subplots(figsize=(10, 10), nrows=1, ncols=2)

    for i, scene in enumerate(scenes):
        title = scene['title']
        light_source = scene['light_source']
        intersections = scene['intersections']
        objects = scene['objects']
        bvh = scene['bvh']

        ax[i].set_title(title)
                
        # Plot the objects (line segments and circles)
        plot_objects(ax[i], objects)

        # Plot the bounding boxes
        plot_bvh(ax[i], bvh)
        
        # Plot the rays and their intersection points
        plot_ray_intersections(ax[i], light_source, intersections)

        # Plot the light source
        ax[i].scatter(light_source.x, light_source.y, c='yellow', s=100, label='Light Source')

        ax[i].set_aspect('equal', adjustable='box')
        ax[i].legend()

    plt.show()

def plot_objects(ax, objects: list[Intersectable]) -> None:
    for obj in objects:
        if isinstance(obj, LineSegment):
            ax.plot([obj.start.x, obj.end.x], [obj.start.y, obj.end.y], c='black', lw=2)
        elif isinstance(obj, Circle):
            circle = plt.Circle((obj.center.x, obj.center.y), obj.radius, color='black', fill=False, lw=2)
            ax.add_patch(circle)

def plot_ray_intersections(ax, light_source: Point, intersections: list[Point]) -> None:
    for intersection in intersections:
        ax.plot([light_source.x, intersection.x], [light_source.y, intersection.y], c='blue', alpha=0.5)
    ax.scatter([i.x for i in intersections], [i.y for i in intersections], c='red', label='Intersections')

def plot_bvh(ax, bvh: BVHNode) -> None:
    def plot_bvh_node(node):
        if isinstance(node, BVHNode):
            colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
            color = random.choice(colors)

            node.aabb.plot(ax, alpha=0.1, color=color)
            if isinstance(node.left, BVHNode):
                plot_bvh_node(node.left)
            if isinstance(node.right, BVHNode):
                plot_bvh_node(node.right)
    
    plot_bvh_node(bvh)

if __name__ == "__main__":
    light_source = Point(0, 0)
    objects = [
        Circle(Point(-2, 2), 0.5),
        Circle(Point(3, -1), 0.5),
        Circle(Point(-2, 0), 0.5),
        Circle(Point(3, 1), 0.5),
        Circle(Point(-2, -2), 0.5),
        Circle(Point(-3.5,0), 0.5),
    ]

    bvh_unbalanced = BVHNode(objects, use_midpoint=False)
    bvh_balanced = BVHNode(objects, use_midpoint=True)
    print("Unbalanced BVH Tree:")
    bvh_unbalanced.printTree()

    print("\nBalanced BVH Tree:")
    bvh_balanced.printTree()

    unbalanced_rays = cast_rays(light_source, bvh_unbalanced)
    balanced_rays = cast_rays(light_source, bvh_balanced)

    print("\t\t\t\tUnbalanced\tBalanced")
    print("Total intersection calls:\t{}\t\t{}".format(unbalanced_rays[2], balanced_rays[2]))
    print("Avg intersection calls per ray:\t{:.2f}\t\t{:.2f}".format(unbalanced_rays[3], balanced_rays[3]))

    scenes = [
        {
            'title': 'Unbalanced BVH Tree',
            'light_source': light_source,
            'intersections': unbalanced_rays[1],
            'objects': objects,
            'bvh': bvh_unbalanced
        },
        {
            'title': 'Balanced BVH Tree',
            'light_source': light_source,
            'intersections': balanced_rays[1],
            'objects': objects,
            'bvh': bvh_balanced
        }
    ]
    
    plot_scenes(scenes)