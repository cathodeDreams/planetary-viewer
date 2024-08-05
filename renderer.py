import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from config import Config
from planet import Planet
from camera import Camera

class Renderer:
    """
    Handles the rendering of the planetary viewer using OpenGL.
    """

    def __init__(self, config: Config):
        """
        Initialize the renderer with the given configuration.

        Args:
            config (Config): Configuration object containing rendering settings.
        """
        self.config = config
        self._setup_pygame()
        self._setup_opengl()

    def _setup_pygame(self):
        """
        Set up Pygame for display and user input.
        """
        pygame.init()
        pygame.display.set_mode((self.config.width, self.config.height), pygame.OPENGL | pygame.DOUBLEBUF | (pygame.FULLSCREEN if self.config.fullscreen else 0))
        pygame.display.set_caption("Planetary Viewer")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def _setup_opengl(self):
        """
        Set up OpenGL rendering context and initial state.
        """
        glViewport(0, 0, self.config.width, self.config.height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Set up projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.config.fov, self.config.width / self.config.height, self.config.near, self.config.far)
        glMatrixMode(GL_MODELVIEW)

    def render(self, planet: Planet, camera: Camera, time: float):
        """
        Render the scene with the given planet, camera, and time.

        Args:
            planet (Planet): The planet object to render.
            camera (Camera): The camera object defining the view.
            time (float): The current simulation time.
        """
        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up the camera
        glLoadIdentity()
        gluLookAt(*camera.position, *camera.target, *camera.up)

        # Update light position for day/night cycle
        self._update_lighting(time)

        # Draw the planet
        planet.draw()

        # Swap the display buffers
        pygame.display.flip()

    def _update_lighting(self, time: float):
        """
        Update the lighting based on the time of day.

        Args:
            time (float): The current simulation time.
        """
        # Calculate light position based on time
        angle = (time % self.config.day_length) / self.config.day_length * 2 * math.pi
        light_x = math.cos(angle)
        light_y = 0.2  # Slight angle from horizontal
        light_z = math.sin(angle)
        glLightfv(GL_LIGHT0, GL_POSITION, (light_x, light_y, light_z, 0))

        # Adjust ambient light based on time of day
        day_factor = (math.sin(angle) + 1) / 2  # 0 to 1
        ambient = 0.2 + 0.2 * day_factor
        glLightfv(GL_LIGHT0, GL_AMBIENT, (ambient, ambient, ambient, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))