import numpy as np

def compute_direct_shading_factor(image, direct_irradiance, image_coords, poly_incident_angle_to_radius, principal_point):
    assert len(direct_irradiance) == len(image_coords), "It seems that the list of direct irradiance values does not coincide with the list of image coordinates!"

    compensated_irradiance_percentage = np.zeros(len(direct_irradiance))