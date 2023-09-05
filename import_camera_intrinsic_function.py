import yaml
import torch
import numpy as np
import cv2
import os

from omnicalib.projection import project_poly_thetar
from camera_coords_to_image_intrinsic import camera_coords_to_image_intrinsic
from read_image_file import read_image_file

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
    fov_limit = camera_coords_to_image_intrinsic(np.array([x_prime,y_prime]).T.tolist(), poly_incident_angle_to_radius, principal_point)

    # the farthest point from the principal point is considered to be the limit
    # this is MY OPINION, I think that the poly_project_thetar would start to loop the angles back when it starts exceeding the FOV
    index_of_max = np.argmax(np.transpose(fov_limit - principal_point))
    estimated_fov = 20 + index_of_max
    # distance_fov = math.sqrt((principal_point_array - fov_limit) ** 2 + (principal_point_array - fov_limit) ** 2)

    # we took one calibration image at random to draw the FOV circle as debug
    files = os.listdir('./CalibrationImages')
    image = cv2.imread("./CalibrationImages/" + files[0])
    im_height, im_width, channels = image.shape

    distance_to_fov = fov_limit[index_of_max][0]-principal_point[0]

    # draw the FOV circle
    image = cv2.circle(image, (round(principal_point[0]),round(principal_point[1])), round(distance_to_fov), (0,0,255), 2)

    # write some FOV numbers in the 8 edges, they could not have possible made it so bad that it clip through all of these
    image = cv2.putText(image, str(estimated_fov), (round(principal_point[0] + distance_to_fov), round(principal_point[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov), (round(principal_point[0] - distance_to_fov), round(principal_point[1])),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov), (round(principal_point[0]), round(principal_point[1] - distance_to_fov)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov), (round(principal_point[0]), round(principal_point[1] + distance_to_fov)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov),
                        (round(principal_point[0] + distance_to_fov/np.sqrt(2)), round(principal_point[1] + distance_to_fov/np.sqrt(2))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov),
                        (round(principal_point[0] - distance_to_fov/np.sqrt(2)), round(principal_point[1] + distance_to_fov/np.sqrt(2))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov),
                        (round(principal_point[0] + distance_to_fov/np.sqrt(2)), round(principal_point[1] - distance_to_fov/np.sqrt(2))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    image = cv2.putText(image, str(estimated_fov),
                        (round(principal_point[0] - distance_to_fov/np.sqrt(2)), round(principal_point[1] - distance_to_fov/np.sqrt(2))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imwrite('./DebugData/fov_test.jpg', image)

    return poly_incident_angle_to_radius, principal_point, estimated_fov