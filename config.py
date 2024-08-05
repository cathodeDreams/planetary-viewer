from pydantic import BaseModel, Field, field_validator

class Config(BaseModel):
    # Window settings
    width: int = Field(2560, ge=800, le=7680, description="Window width in pixels")
    height: int = Field(1440, ge=600, le=4320, description="Window height in pixels")
    fullscreen: bool = Field(True, description="Whether to run in fullscreen mode")
    fps: int = Field(165, ge=30, le=240, description="Target frames per second")

    # Camera settings
    fov: float = Field(60.0, ge=30.0, le=120.0, description="Field of view in degrees")
    near: float = Field(0.1, gt=0, description="Near clipping plane distance")
    far: float = Field(1000.0, gt=100, description="Far clipping plane distance")
    initial_distance: float = Field(30.0, ge=10.0, le=100.0, description="Initial camera distance from planet center")
    max_distance: float = Field(50.0, ge=20.0, le=200.0, description="Maximum camera distance from planet center")
    mouse_sensitivity: float = Field(0.005, ge=0.001, le=0.1, description="Mouse sensitivity for camera control")
    zoom_speed: float = Field(0.5, ge=0.1, le=2.0, description="Camera zoom speed")
    camera_speed: float = Field(0.1, ge=0.01, le=1.0, description="Camera movement speed in free mode")
    camera_boost_factor: float = Field(2.0, ge=1.1, le=5.0, description="Speed multiplier when boost is active")

    # Planet settings
    planet_radius: float = Field(10.0, ge=1.0, le=50.0, description="Radius of the planet")
    texture_width: int = Field(512, ge=512, le=8192, description="Width of the planet texture")
    texture_height: int = Field(256, ge=256, le=4096, description="Height of the planet texture")
    sphere_detail: int = Field(100, ge=20, le=1000, description="Level of detail for the planet sphere")

    # Simulation settings
    day_length: float = Field(3600.0, ge=10.0, le=3600.0, description="Length of a day in seconds")

    @field_validator('max_distance')
    def max_distance_must_be_greater_than_initial(cls, v, values):
        if 'initial_distance' in values and v <= values['initial_distance']:
            raise ValueError('max_distance must be greater than initial_distance')
        return v

    @field_validator('far')
    def far_must_be_greater_than_near(cls, v, values):
        if 'near' in values and v <= values['near']:
            raise ValueError('far must be greater than near')
        return v

    class Config:
        arbitrary_types_allowed = True