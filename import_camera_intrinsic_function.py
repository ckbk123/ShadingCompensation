from yaml import load, SafeLoader
from numpy import tan, linspace, zeros, pi, array, argmax, transpose, sqrt
from cv2 import circle, imread, imwrite, putText, FONT_HERSHEY_SIMPLEX, LINE_AA
from os import listdir

from camera_coords_to_image_intrinsic import camera_coords_to_image_intrinsic
from colorama import Fore, Style

# this function import the data and estimate the fov of the camera
# note that if the FOV is above 89 it wouldnt know
# poly_incident_angle_to_radius is a numpy array
# principal point is a numpy array
# estimated_fov is the estimated FOV in DEGREES
def import_camera_intrinsic_function():
    try:
        with open('calibration.yml') as f:
            data = load(f, Loader=SafeLoader)
            poly_incident_angle_to_radius = data['poly_incident_angle_to_radius']
            principal_point = data['principal_point']
            f.close()
    except EnvironmentError:
        print('It seems that no camera calibration data was available. Please check for calibration.yml')

    ###################### ESTIMATE LENS FOV ######################
    print(f"{Fore.YELLOW}Estimating your lens FOV...{Style.RESET_ALL}")
    fov_test_theta = linspace(20,89,70)*pi/180    # probably wont have any thing worse than 20degs, hopefully ur not using one this bad for this work lol

    # directly estimate x_prime and y_prime (z_prime all =1) because this conversion is simple
    x_prime = tan(fov_test_theta)
    y_prime = zeros(len(fov_test_theta))

    # use the camera_coords_to_image_intrinsic to determine how all these points map onto the image
    fov_limit = camera_coords_to_image_intrinsic(array([x_prime,y_prime]).T.tolist(), poly_incident_angle_to_radius, principal_point)

    # the farthest point from the principal point is considered to be the limit
    # this is MY OPINION, I think that the poly_project_thetar would start to loop the angles back when it starts exceeding the FOV
    index_of_max = argmax(transpose(fov_limit - principal_point))
    estimated_fov = 20 + index_of_max
    # distance_fov = math.sqrt((principal_point_array - fov_limit) ** 2 + (principal_point_array - fov_limit) ** 2)

    # we took one calibration image at random to draw the FOV circle as debug
    files = listdir('./CalibrationImages')
    image = imread("./CalibrationImages/" + files[0])
    im_height, im_width, channels = image.shape

    distance_to_fov = fov_limit[index_of_max][0]-principal_point[0]

    # draw the FOV circle
    image = circle(image, (round(principal_point[0]),round(principal_point[1])), round(distance_to_fov), (0,0,255), 2)

    # write some FOV numbers in the 8 edges, they could not have possible made it so bad that it clip through all of these
    image = putText(image, str(estimated_fov), (round(principal_point[0] + distance_to_fov), round(principal_point[1])),
                            FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, LINE_AA)

    image = putText(image, str(estimated_fov), (round(principal_point[0] - distance_to_fov), round(principal_point[1])),
                            FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov), (round(principal_point[0]), round(principal_point[1] - distance_to_fov)),
                            FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov), (round(principal_point[0]), round(principal_point[1] + distance_to_fov)),
                            FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov),
                        (round(principal_point[0] + distance_to_fov/sqrt(2)), round(principal_point[1] + distance_to_fov/sqrt(2))),
                        FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov),
                        (round(principal_point[0] - distance_to_fov/sqrt(2)), round(principal_point[1] + distance_to_fov/sqrt(2))),
                        FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov),
                        (round(principal_point[0] + distance_to_fov/sqrt(2)), round(principal_point[1] - distance_to_fov/sqrt(2))),
                        FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    image = putText(image, str(estimated_fov),
                        (round(principal_point[0] - distance_to_fov/sqrt(2)), round(principal_point[1] - distance_to_fov/sqrt(2))),
                        FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, LINE_AA)

    imwrite('./DebugData/fov_test.jpg', image)
    print(f"{Fore.GREEN}Estimated FOV is " + str(estimated_fov) + f"°. {Fore.LIGHTCYAN_EX}You should check out fov_test.jpg in DebugData to ensure that the FOV circle lines up with the border of your fisheye view!{Style.RESET_ALL}")

    return poly_incident_angle_to_radius, principal_point, estimated_fov