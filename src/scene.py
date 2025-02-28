from config import *
import sphere
from src import camera
import plane
import light

class Scene:
    """
        Holds pointers to all objects in the scene
    """


    def __init__(self):
        """
            Set up scene objects.
        """
        
        self.spheres = [
            sphere.Sphere(
                center = [
                    np.random.uniform(low = -2.0, high = 2.0),
                    np.random.uniform(low = -2.0, high = 2.0),
                    np.random.uniform(low = -4.0, high = 4.0)
                ],
                radius = np.random.uniform(low = 0.3, high = 1.0),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ],
                roughness = np.random.uniform(low = 0.3, high = 0.8)
            ) for i in range(2)
        ]
        
        self.planes = [
            plane.Plane(
                normal = [0, 0, 1],
                tangent = [1, 0, 0],
                bitangent = [0, 1, 0],
                uMin = -0.5,
                uMax = 1.0,
                vMin = -0.5,
                vMax = 1.0,
                center = [i % 3, -1 + i // 3, -1],
                material_index = i
            ) for i in range(9)
        ]

        self.lights = [
            light.Light(
                position = [
                    np.random.uniform(low = -1.0, high = 3.0),
                    np.random.uniform(low = -1.0, high = 3.0),
                    np.random.uniform(low = -5.0, high = 5.0)
                ],
                strength = np.random.uniform(low = 1.0, high = 3.0),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ],
            ) for i in range(4)
        ]

        self.objectCounts = np.array(
            [len(self.spheres), len(self.planes), len(self.lights)], 
            dtype = np.int32)
        
        self.camera = camera.Camera(
            position = [-1, 0, 0]
        )

        self.outDated = True
    
    def move_player(self, forwardsSpeed: float, rightSpeed: float) -> None:
        """
        attempt to move the player with the given speed
        """
        
        dPos = forwardsSpeed * self.camera.forwards + rightSpeed * self.camera.right
        
        self.camera.position[0] += dPos[0]
        self.camera.position[1] += dPos[1]
    
    def spin_player(self, dAngle: list[float, float]) -> None:
        """
            shift the player's direction by the given amount, in degrees
        """
        self.camera.theta += dAngle[0]
        if (self.camera.theta < 0):
            self.camera.theta += 360
        elif (self.camera.theta > 360):
            self.camera.theta -= 360
        
        self.camera.phi += dAngle[1]
        if (self.camera.phi < -89):
            self.camera.phi = -89
        elif (self.camera.phi > 89):
            self.camera.phi = 89
        
        self.camera.recalculateVectors()