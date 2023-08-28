import yaml
import torch
import numpy as np

from omnicalib.projection import project_poly_thetar
import camera_coords_to_image_intrinsic as intrinsic

# this function import the data and estimate the fov of the camera
# note that if the FOV is above 89 it wouldnt know
# poly_incident_angle_to_radius is a numpy array
# principal point is a numpy array
# estimated_fov is the estimated FOV in DEGREES
def import_camera_intrinsic_function():
    try:
        with open('calibration.yml') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            poly_incident_angle_to_radius = data['poly_incident_angle_to_radius']
            principal_point = data['principal_point']
            f.close()
    except EnvironmentError:
        print('It seems that no camera calibration data was available. Please check for calibration.yml')

    ###################### ESTIMATE LENS FOV ######################
    fov_test_theta = np.linspace(20,89,70)*np.pi/180    # probably wont have any thing worse than 20degs, hopefully ur not using one this bad for this work lol

    # directly estimate x_prime and y_prime (z_prime all =1) because this conversion is simple
    x_prime = np.tan(fov_test_theta)
    y_prime = np.zeros(len(fov_test_theta))

    # use the camera_coords_to_image_intrinsic to determine how all these points map onto the image
    fov_limit = intrinsic.camera_coords_to_image_intrinsic(np.array([x_prime,y_prime]).T.tolist(), poly_incident_angle_to_radius, principal_point)

    # the farthest point from the principal point is considered to be the limit
    # this is MY OPINION, I think that the poly_project_thetar would start to loop the angles back when it starts exceeding the FOV
    estimated_fov = 20 + np.argmax(np.transpose(fov_limit - principal_point))
    # distance_fov = math.sqrt((principal_point_array - fov_limit) ** 2 + (principal_point_array - fov_limit) ** 2)

    return poly_incident_angle_to_radius, principal_point, estimated_fov