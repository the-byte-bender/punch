def convert_to_openal_coordinates(
    x: float, y: float, z: float
) -> tuple[float, float, float]:
    """convert coordinates from a right handed coordinate system where positive x is right, positive y is forward and positive z is up, to the OpenAL coordinate system."""
    openal_x = x  # No change in x-axis
    openal_y = z  # Swap y and z axes
    openal_z = -y  # Invert y-axis
    return openal_x, openal_y, openal_z
