from math import cos, sin , pi , atan2 , sqrt
import time
from random import random , uniform
import numpy as np
import pygame

def display_image(image_array):
    # Determine image dimensions
    height, width, _ = image_array.shape

    # Initialize Pygame
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Image Display")

    # Create black surface
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    for x in range(height):
        for y in range(width):
            # Get the color of the pixel
            color = image_array[y, x]
            color = (int(color[0]), int(color[1]), int(color[2]))
            # Draw the pixel
            pygame.draw.rect(background, color, (x, y, 1, 1))
    
    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    # Wait for the window to be closed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Quit Pygame
    pygame.quit()


class Point3D:
    def __init__(self, x: int, y: int , z: int):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def move(self, dx: int, dy: int, dz: int):
        self.x += dx
        self.y += dy
        self.z += dz
        
    def __truediv__(self, scalar):
        return Point3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self
    
    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __mul__(self, scalar):
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self
    
    def normalize(self):
        magnitude = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude
        
    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"
    
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
def subtract_vectors(v1, v2):
    return Point3D(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def cross_product(v1, v2):
    return Point3D(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)

def scalar_multiply(vector, scalar):
    return Point3D(vector.x * scalar, vector.y * scalar, vector.z * scalar)

def random_vector():
    return Point3D(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
        

def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
            
def mix_colors(color1, color2, ratio):
    # Ensure ratio is between 0 and 1
    ratio = max(0, min(ratio, 1))

    # Calculate the mixed color components
    mixed_color = (
        color1[0] * (1 - ratio) + color2[0] * ratio,
        color1[1] * (1 - ratio) + color2[1] * ratio,
        color1[2] * (1 - ratio) + color2[2] * ratio
    )

    return mixed_color


class Simple3DObject:
    def __init__(self, points):
        self.points = points
    
    def is_point_inside(self, x: float, y: float, z: float):
        # fast algorithm to check if a point is inside the object
        max_x = max([point.x for point in self.points])
        min_x = min([point.x for point in self.points])
        max_y = max([point.y for point in self.points])
        min_y = min([point.y for point in self.points])
        max_z = max([point.z for point in self.points])
        min_z = min([point.z for point in self.points])
        return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z
    
    def __str__(self):
        return f"Simple3DObject with {len(self.points)} vertices"
    
    def move(self, dx: int, dy: int, dz: int):
        for point in self.points:
            point.move(dx, dy, dz)
            
    def rotate(self, angle: float , axis = 'x'):
        # rotate the object around the x-axis
        for point in self.points:
            if axis == 'x':
                y = point.y
                z = point.z
                point.y = y * cos(angle) - z * sin(angle)
                point.z = y * sin(angle) + z * cos(angle)
            elif axis == 'y':
                x = point.x
                z = point.z
                point.x = x * cos(angle) - z * sin(angle)
                point.z = x * sin(angle) + z * cos(angle)
            elif axis == 'z':
                x = point.x
                y = point.y
                point.x = x * cos(angle) - y * sin(angle)
                point.y = x * sin(angle) + y * cos(angle)
            else:
                raise ValueError("Invalid axis")
            
    def scale (self, factor: float):
        for point in self.points:
            point.x *= factor
            point.y *= factor
            point.z *= factor
            
            
def dim_color_over_distance(factor , color , distance):
    return tuple([int(color[i] * factor ** distance) for i in range(3)])
            
class Material:
    def __init__(self, color: tuple = (255,255,255), shininess: float = 0.5 , roughness = 0.5):
        self.color = color
        self.shininess = shininess
        self.roughness = roughness
        
    def __str__(self):
        return f"Material with color {self.color}, shininess {self.shininess}, and roughness {self.roughness}"
        
class Cube(Simple3DObject):
    def __init__(self, x: int, y: int, z: int, side_length: int , material: Material = Material()):
        self.side_length = side_length
        self.points = [
            Point3D(x, y, z),
            Point3D(x + side_length, y, z),
            Point3D(x + side_length, y + side_length, z),
            Point3D(x, y + side_length, z),
            Point3D(x, y, z + side_length),
            Point3D(x + side_length, y, z + side_length),
            Point3D(x + side_length, y + side_length, z + side_length),
            Point3D(x, y + side_length, z + side_length)
        ]
        self.faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 3, 7, 4),
            (1, 2, 6, 5)
        ]
        self.material = material
        # super().__init__(points)
    
    def __str__(self):
        return f'Position of the cube is :  {self.points}'
    
    def expand_x(self,factor):
        self.side_length *= factor
        for point in self.points:
            point.x *= factor
    
    def expand_y(self,factor):
        self.side_length *= factor
        for point in self.points:
            point.y *= factor
    
    def expand_z(self,factor):
        self.side_length *= factor
        for point in self.points:
            point.z *= factor
    
        

def covert_3d_angles_to_vector(roll: float, pitch: float, yaw: float):
    # convert 3D angles to vector
    x = cos(roll) * cos(pitch)
    y = sin(roll) * cos(pitch)
    z = -sin(pitch)
    return x, y, z

def convert_vector_to_3d_angles(x: float, y: float, z: float):
    # convert vector to 3D angles
    yaw = atan2(y, x)
    pitch = atan2(-z, sqrt(x * x + y * y))
    roll = atan2(sin(yaw) * y + cos(yaw) * x, cos(yaw) * y - sin(yaw) * x)
    return roll, pitch, yaw

        
class CameraRayCasting():
    def __init__(self, camera_position: Point3D, camera_direction: Point3D, scene_objects: list[Simple3DObject]):
        self.camera_position = camera_position
        self.camera_direction = camera_direction
        self.scene_objects = scene_objects
        
    # Assuming necessary imports are done

    def render(self, num_rays: int = 64, max_distance: int = 50, direction: dict = {'x': 0, 'y': 0, 'z': 1}, fov=30, aspect_ratio=1/1, step=1, number_of_reflections=32):
        width = int(num_rays * aspect_ratio)
        height = num_rays

        screen = np.zeros((height, width, 3))

        # Convert direction vector to roll, pitch, and yaw angles
        direction_vector = Point3D(direction['x'], direction['y'], direction['z'])

        for h in range(height):
            for w in range(width):
                # Calculate the normalized screen coordinates
                x = (w + 0.5) / width
                y = (h + 0.5) / height

                normalized_x = (x - 0.5) * fov
                normalized_y = (y - 0.5) * fov

                # Calculate the direction of the ray relative to camera orientation
                ray_direction = direction_vector + Point3D(normalized_x, normalized_y, 0)

                hit_object = False

                for distance in range(0, max_distance, step):
                    if hit_object:
                        break

                    next_point = self.camera_position + scalar_multiply(ray_direction, distance)


                    # Check for intersection with each object in the scene
                    for obj in self.scene_objects:
                        if obj.is_point_inside(next_point.x, next_point.y, next_point.z):
                            hit_object = True
                            # Get object material properties
                            primary_color = obj.material.color
                            primary_shininess = obj.material.shininess
                            primary_roughness = obj.material.roughness

                            # Cast ray in all directions to find reflections
                            accumulated_color = primary_color
                            for i in range(number_of_reflections):
                                # for face in obj.faces:
                                    # # Get the normal of the face
                                    # v1 = obj.points[face[1]]
                                    # v2 = obj.points[face[2]]
                                    # v3 = obj.points[face[3]]
                                    # normal = cross_product(subtract_vectors(v2, v1), subtract_vectors(v3, v1))
                                    # normal_length = normal.magnitude()
                                    # normal /= normal_length

                                    # # Calculate the reflection direction
                                    # dot = dot_product(ray_direction, normal)
                                    # reflection_direction = ray_direction - scalar_multiply(normal, 2 * dot)

                                    # # Add randomness to the reflection direction based on the roughness
                                    reflection_direction = scalar_multiply(random_vector(), primary_roughness)
                                    reflection_direction.normalize()

                                    # Cast the reflection ray
                                    reflection_hit = False
                                    for dis in range(1,max_distance):
                                        reflection_point = next_point + reflection_direction * dis
                                        if obj.is_point_inside(reflection_point.x, reflection_point.y, reflection_point.z):
                                            secondary_color = obj.material.color
                                            if secondary_color != primary_color:
                                                print('secondary color' , secondary_color)
                                                print('primary color' , primary_color)
                                            # Calculate the color of the pixel based on the material properties like shininess and color
                                            accumulated_color = mix_colors(accumulated_color, secondary_color, primary_shininess)
                                            reflection_hit = True
                                            break
                                    if reflection_hit:
                                        break

                            screen[h][w] = dim_color_over_distance(0.95, accumulated_color, distance)
                            break

        return screen



                        
        

# Example usage:
# points = [
#     Point3D(0, 0, 0),
#     Point3D(1, 0, 0),
#     Point3D(1, 1, 0),
#     Point3D(0, 1, 0),
#     Point3D(0, 0, 1),
#     Point3D(1, 0, 1),
#     Point3D(1, 1, 1),
#     Point3D(0, 1, 1)
# ]

cube = Cube(0, 0, 16, 5 , Material((255, 0, 0) , 0.5 , 0.1))
print(cube)
cube2 = Cube(0, 0, 10, 2 , Material((0, 255, 0) , 0.5 , 0.75))
print(cube)
cube3 = Cube(-2, 0, 13, 2 , Material((0, 0, 255) , 0.5 , 0.25))
cube4 = Cube(2, 0, 1, 1 , Material((0, 255, 255) , 0.5 , 0.9))
cube4.expand_z(5)

# cube = Simple3DObject(points)
# cube.move(0,0,10)

# Check if a point is inside the cube
# point_to_check = Point3D(0.5, 0.5, 0.5)
# print(cube.is_point_inside(point_to_check.x, point_to_check.y, point_to_check.z))

camera = CameraRayCasting(Point3D(0, 0, 0), Point3D(0, 0, 1), [cube,cube2,cube3,cube4])
start = time.time()
render = camera.render(num_rays=200, max_distance=20, direction={'x': 0, 'y': 0, 'z': 1}, fov=1.5, aspect_ratio=1/1, step=1, number_of_reflections=16)
display_image(render)
print('render took :', time.time() - start , 'seconds')