from OpenGL.GL import *
from OpenGL.GLU import *
from config import Config
from texture_generator import TextureGenerator
import numpy as np

class Planet:
    """
    Represents a planet with a textured sphere in 3D space.
    """

    def __init__(self, config: Config):
        """
        Initialize the planet with the given configuration.

        Args:
            config (Config): Configuration object containing planet settings.
        """
        self.config = config
        self.radius = config.planet_radius
        self.texture = self._load_texture()
        self.sphere = self._create_sphere()

    def _load_texture(self):
        """
        Load and create the planet's texture.

        Returns:
            int: OpenGL texture ID.

        Raises:
            RuntimeError: If texture generation or loading fails.
        """
        try:
            img = TextureGenerator.generate(self.config.texture_width, self.config.texture_height)
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())
            return texture_id
        except Exception as e:
            raise RuntimeError(f"Failed to load planet texture: {str(e)}")

    def _create_sphere(self):
        """
        Create a GLU quadric object for rendering the planet sphere.

        Returns:
            GLUquadric: GLU quadric object for the planet sphere.
        """
        sphere = gluNewQuadric()
        gluQuadricNormals(sphere, GLU_SMOOTH)
        gluQuadricTexture(sphere, GL_TRUE)
        return sphere

    def draw(self):
        """
        Draw the planet using OpenGL.
        """
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)  # Rotate to show poles correctly
        gluSphere(self.sphere, self.radius, self.config.sphere_detail, self.config.sphere_detail)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)