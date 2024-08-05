import numpy as np
from math import cos, sin, pi
from config import Config

class Camera:
    """
    Represents a camera in 3D space with orbit and free movement modes.
    """

    def __init__(self, config: Config):
        """
        Initialize the camera with the given configuration.

        Args:
            config (Config): Configuration object containing camera settings.
        """
        self.config = config
        self.distance = config.initial_distance
        self.yaw = 0
        self.pitch = 0
        self.position = np.array([0.0, 0.0, self.distance])
        self.target = np.zeros(3)
        self.up = np.array([0.0, 1.0, 0.0])
        self.mode = 'orbit'
        self.speed = config.camera_speed
        self.boost_factor = config.camera_boost_factor
        self.transition_progress = 1.0
        self.transition_duration = 1.0  # seconds
        self.start_position = self.position.copy()
        self.start_target = self.target.copy()
        self.end_position = self.position.copy()
        self.end_target = self.target.copy()

    def update(self, dx: float, dy: float, dt: float):
        """
        Update the camera position based on mouse movement and elapsed time.

        Args:
            dx (float): Mouse movement in x-direction.
            dy (float): Mouse movement in y-direction.
            dt (float): Elapsed time since last update.
        """
        if self.mode == 'orbit':
            self._update_orbit(dx, dy)
        elif self.mode == 'free':
            self._update_free(dx, dy)
        
        self._update_transition(dt)

    def _update_orbit(self, dx: float, dy: float):
        """
        Update camera position in orbit mode.

        Args:
            dx (float): Mouse movement in x-direction.
            dy (float): Mouse movement in y-direction.
        """
        self.yaw += dx * self.config.mouse_sensitivity
        self.pitch -= dy * self.config.mouse_sensitivity
        self.pitch = np.clip(self.pitch, -pi/2 + 0.1, pi/2 - 0.1)
        self._update_position()

    def _update_free(self, dx: float, dy: float):
        """
        Update camera orientation in free mode.

        Args:
            dx (float): Mouse movement in x-direction.
            dy (float): Mouse movement in y-direction.
        """
        self.yaw -= dx * self.config.mouse_sensitivity
        self.pitch -= dy * self.config.mouse_sensitivity
        self.pitch = np.clip(self.pitch, -pi/2 + 0.1, pi/2 - 0.1)
        
        forward = self._get_forward_vector()
        self.target = self.position + forward

    def _get_forward_vector(self):
        """
        Calculate and return the forward vector based on yaw and pitch.

        Returns:
            np.array: The forward vector.
        """
        return np.array([
            cos(self.pitch) * sin(self.yaw),
            sin(self.pitch),
            cos(self.pitch) * cos(self.yaw)
        ])

    def move(self, forward: float, right: float, up: float, boost: bool):
        """
        Move the camera in free mode.

        Args:
            forward (float): Amount of forward movement.
            right (float): Amount of right movement.
            up (float): Amount of upward movement.
            boost (bool): Whether to apply speed boost.
        """
        if self.mode != 'free':
            return

        speed = self.speed * (self.boost_factor if boost else 1)
        
        forward_vec = self._get_forward_vector()
        right_vec = np.cross(forward_vec, self.up)
        right_vec /= np.linalg.norm(right_vec)

        movement = forward_vec * forward + right_vec * right + self.up * up
        self.position += movement * speed
        self.target += movement * speed

    def zoom(self, amount: float):
        """
        Zoom the camera in or out.

        Args:
            amount (float): Amount of zoom. Positive values zoom in, negative values zoom out.
        """
        if self.mode == 'orbit':
            self.distance -= amount * self.config.zoom_speed
            self.distance = np.clip(self.distance, self.config.planet_radius + 0.1, self.config.max_distance)
            self._update_position()
        elif self.mode == 'free':
            self.move(amount * self.config.zoom_speed, 0, 0, False)

    def _update_position(self):
        """
        Update the camera position based on distance, yaw, and pitch in orbit mode.
        """
        self.position = np.array([
            self.distance * cos(self.pitch) * sin(self.yaw),
            self.distance * sin(self.pitch),
            self.distance * cos(self.pitch) * cos(self.yaw)
        ])

    def toggle_mode(self):
        """
        Toggle between orbit and free camera modes.
        """
        if self.mode == 'orbit':
            self.mode = 'free'
            # When switching to free mode, keep the same position and target
            self.end_position = self.position.copy()
            self.end_target = self.target.copy()
        else:
            self.mode = 'orbit'
            # When switching back to orbit mode, reset to initial values
            self.distance = self.config.initial_distance
            self.yaw = 0
            self.pitch = 0
            self._update_position()
            self.end_position = self.position.copy()
            self.end_target = np.zeros(3)
        
        self.start_position = self.position.copy()
        self.start_target = self.target.copy()
        self.transition_progress = 0.0

    def _update_transition(self, dt: float):
        """
        Update the transition between camera modes.

        Args:
            dt (float): Elapsed time since last update.
        """
        if self.transition_progress < 1.0:
            self.transition_progress = min(1.0, self.transition_progress + dt / self.transition_duration)
            t = self._ease_in_out_cubic(self.transition_progress)
            self.position = self.start_position * (1 - t) + self.end_position * t
            self.target = self.start_target * (1 - t) + self.end_target * t

    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        """
        Apply cubic easing to a value between 0 and 1.

        Args:
            t (float): Input value between 0 and 1.

        Returns:
            float: Eased value between 0 and 1.
        """
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

    def check_collision(self, planet_radius: float):
        """
        Check and prevent camera collision with the planet.

        Args:
            planet_radius (float): Radius of the planet.
        """
        distance_to_center = np.linalg.norm(self.position)
        if distance_to_center < planet_radius + 0.1:
            direction = self.position / distance_to_center
            self.position = direction * (planet_radius + 0.1)
            if self.mode == 'orbit':
                self.distance = planet_radius + 0.1