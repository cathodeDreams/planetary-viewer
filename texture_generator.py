import numpy as np
from noise import snoise3
from PIL import Image

class TextureGenerator:
    """
    Generates seamless textures for planetary surfaces.
    """

    @staticmethod
    def generate(width: int, height: int) -> Image.Image:
        """
        Generate a seamless texture for a planetary surface.

        Args:
            width (int): The width of the texture in pixels.
            height (int): The height of the texture in pixels.

        Returns:
            Image.Image: The generated texture as a PIL Image.

        Raises:
            ValueError: If width or height are not positive integers.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")

        try:
            # Generate base and detail noise
            base = TextureGenerator._create_seamless_noise(width, height, scale=4.0, octaves=6, persistence=0.5)
            detail = TextureGenerator._create_seamless_noise(width, height, scale=20.0, octaves=8, persistence=0.6)

            # Combine base and detail noise
            combined = (base * 0.7 + detail * 0.3)
            combined = (combined - combined.min()) / (combined.max() - combined.min())

            # Generate random colors for the texture
            color1 = np.random.randint(100, 200, 3)
            color2 = np.random.randint(100, 200, 3)

            # Create the final texture
            texture = TextureGenerator._create_colored_texture(combined, color1, color2)

            return Image.fromarray(texture)
        except Exception as e:
            raise RuntimeError(f"Failed to generate texture: {str(e)}")

    @staticmethod
    def _create_seamless_noise(width: int, height: int, scale: float = 50.0, octaves: int = 6, 
                               persistence: float = 0.5, lacunarity: float = 2.0) -> np.ndarray:
        """
        Create a seamless noise texture using 3D Simplex noise.

        Args:
            width (int): The width of the texture in pixels.
            height (int): The height of the texture in pixels.
            scale (float): The scale of the noise.
            octaves (int): The number of octaves for the noise.
            persistence (float): The persistence for each octave.
            lacunarity (float): The lacunarity for each octave.

        Returns:
            np.ndarray: The generated seamless noise.
        """
        world = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                theta = x / width * 2 * np.pi
                phi = y / height * np.pi
                x3 = np.cos(theta) * np.sin(phi)
                y3 = np.sin(theta) * np.sin(phi)
                z3 = np.cos(phi)
                world[y][x] = snoise3(x3 * scale, y3 * scale, z3 * scale, 
                                      octaves=octaves, persistence=persistence, lacunarity=lacunarity)
        return world

    @staticmethod
    def _create_colored_texture(noise: np.ndarray, color1: np.ndarray, color2: np.ndarray) -> np.ndarray:
        """
        Create a colored texture from noise data and two colors.

        Args:
            noise (np.ndarray): The noise data.
            color1 (np.ndarray): The first color as an RGB array.
            color2 (np.ndarray): The second color as an RGB array.

        Returns:
            np.ndarray: The colored texture as a 3D numpy array.
        """
        texture = np.zeros((*noise.shape, 3), dtype=np.uint8)
        for y in range(noise.shape[0]):
            for x in range(noise.shape[1]):
                value = noise[y][x]
                color = color1 * (1 - value) + color2 * value
                variation = np.random.uniform(0.99, 1.01, 3)
                texture[y][x] = np.clip(color * variation, 0, 255).astype(np.uint8)
        return texture