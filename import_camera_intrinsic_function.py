import yaml
import torch
import numpy as np

from omnicalib.projection import project_poly_thetar

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
    x_prime = np.multiply(np.cos(0), np.tan(fov_test_theta))
    y_prime = np.multiply(np.sin(0), np.tan(fov_test_theta))
    z_prime = np.ones(len(x_prime))

    # convert the np.array [x_prime, y_prime, z_prime] to a list that could be used in the project_poly_thetar
    # the transpose is to get [x1,x2], [y1,y2], [z1,z2] to [x1,y1,z1], [x2,y2,z2]
    fov_estimate_coords = np.ndarray.tolist( np.matrix.transpose( np.array([x_prime, y_prime, z_prime]) ) )

    # no need to calculate the distance because we fixed azimuth to 0 => it align to the x-axis in the camera reference frames
    fov_limit = project_poly_thetar(torch.Tensor(fov_estimate_coords), poly_incident_angle_to_radius, torch.Tensor(principal_point), False).numpy()

    # the farthest point from the principal point is considered to be the limit
    # this is MY OPINION, I think that the poly_project_thetar would start to loop the angles back when it starts exceeding the FOV
    estimated_fov = 20 + np.argmax(np.transpose(fov_limit - principal_point))
    # distance_fov = math.sqrt((principal_point_array - fov_limit) ** 2 + (principal_point_array - fov_limit) ** 2)

    return poly_incident_angle_to_radius, principal_point, estimated_fov