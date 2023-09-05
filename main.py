# This is a sample Python script.

from astropy_to_camera_extrinsic import astropy_to_camera_extrinsic
from camera_coords_to_image_intrinsic import camera_coords_to_image_intrinsic
from compute_diffuse_shading_factor import compensate_diffuse_irradiance
from compute_direct_shading_factor import compensate_direct_irradiance
from import_camera_intrinsic_function import import_camera_intrinsic_function
from read_image_file import read_image_file
from retrieve_PVGIS_irradiance import retrieve_PVGIS_irradiance
from sunpath_from_astropy import sunpath_from_astropy
from calibrate_camera import calibrate_camera

import numpy as np
import matplotlib.pyplot as plt

import torch as torch

def irradianceforecast():
    # calibrate_camera(6, 9, 22, './CalibrationImagesDebug/*.jpg')

    poly_incident_angle_to_radius, principal_point, estimated_fov = import_camera_intrinsic_function()

    image, im_height, im_width = read_image_file()
    #
    direct_irradiance, diffuse_irradiance, time_array = retrieve_PVGIS_irradiance(43.57, 1.46, 2014, 2015, inclination=8, orientation=42)
    #
    astropy_coords = sunpath_from_astropy(43.57, 1.46, 151, time_array)
    #
    compensated_diffuse = compensate_diffuse_irradiance(image, diffuse_irradiance, poly_incident_angle_to_radius, principal_point, estimated_fov, im_height, im_width)
    #
    compensated_direct = compensate_direct_irradiance(image, im_height, im_width, poly_incident_angle_to_radius, principal_point, 20, 10, estimated_fov, astropy_coords, direct_irradiance, time_array)
    #
    final_irradiance = compensated_direct + compensated_diffuse
    # final_irradiance = direct_irradiance + diffuse_irradiance
    plt.plot(time_array, final_irradiance)
    plt.show()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    irradianceforecast()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
