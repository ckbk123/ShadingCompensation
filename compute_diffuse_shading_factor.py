import numpy as np
import torch
import cv2
from tqdm import tqdm
from omnicalib.projection import project_poly_thetar
import camera_coords_to_image_intrinsic as intrinsic

def compensate_diffuse_irradiance(image, diffuse_irradiance, poly_incident_angle_to_radius, principal_point, estimated_fov):
    print("Calculating diffuse shading factor")

    ## create a photo
    azimuth_length = 1000
    zenith_length = 500
    estimated_fov = estimated_fov*np.pi/180     # convert to RADIANS

    ## so the created photo have around 500 corresponding to the estimated_fov
    ## so what would be the true length with we have 90 perfectly?
    true_90 = zenith_length/(1-np.cos(estimated_fov))

    # construct the array of index to iterate thru azimuth + zenith and the respective blank image
    horizontal_index = np.linspace(0, azimuth_length-1, azimuth_length, True, False, 'int')
    vertical_index = np.linspace(0, zenith_length-1, zenith_length, True, False, 'int')

    # create a blank canvas utilizing the azimuth_length and zenith_length values
    # the dtype=np.unit8 is important to make the imshow function understand how to plot the image.
    conformal_image = np.zeros((zenith_length, azimuth_length), dtype=np.uint8)

    # each point on the conformal image has an equivalent azimuth and zenith
    azimuth_remapped = horizontal_index*2*np.pi/azimuth_length
    zenith_remapped = np.arccos(1-(vertical_index+1)/true_90)

    # create a meshgrid of coordinates. Note that the zenith section is in one mat zenith_mat and azimuth is in the other mat
    zenith_mat, azimuth_mat = np.meshgrid(zenith_remapped, azimuth_remapped, indexing='ij')

    # multiply those two mat to create the max of x_prime and y_prime
    x_prime = np.multiply(np.cos(azimuth_mat), np.tan(zenith_mat))
    y_prime = np.multiply(np.sin(azimuth_mat), np.tan(zenith_mat))

    # stack x_prime and y_prime to create a matrix of coordinate pairs. This could be used directly with intrinsic.camera_coords_to_image_intrinsic
    xy_coord_matrix = np.stack((x_prime,y_prime),axis=2)

    equi_point = intrinsic.camera_coords_to_image_intrinsic(xy_coord_matrix.tolist(), poly_incident_angle_to_radius, principal_point)

    for hor in horizontal_index:
        for ver in vertical_index:
            conformal_image[ver][hor] = image[equi_point[ver][hor][0]][equi_point[ver][hor][1]]

    # write the conformal image for debugging purposes
    cv2.imwrite('./DebugData/conformal_image.jpg', conformal_image)

    # note that we use the true_90 instead of zenith length because this will maximize the shading factor
    diffuse_coeff = (azimuth_length*true_90 - cv2.sumElems(conformal_image)[0] / 255) / (azimuth_length*true_90)

    print('Diffuse shading factor is around ', str(diffuse_coeff))
    return (1-diffuse_coeff)*diffuse_irradiance         # this essentially returns the diffuse component after compensated with shadings