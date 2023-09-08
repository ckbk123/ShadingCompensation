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
from read_user_data import read_user_data
from state_of_charge_estimation import state_of_charge_estimation

from colorama import Fore, Style

import numpy as np
import matplotlib.pyplot as plt

import torch as torch

def irradianceForecast():
    lat, long, elev, orient, incline, vtx_short, vtx_long, calib_sq, st_year, ed_year, solar_peak, conv_eff, charge_eff, discharge_eff, max_soc, min_soc, batt_nom_cap, batt_nom_volt = read_user_data()

    print(f"{Fore.LIGHTRED_EX}INFORMATION: {Fore.LIGHTCYAN_EX}If you run this for the first time, you will need to calibrate the camera. Answer y in the next question initiate a calibration. It will take some times...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}You will see some graphs pop-ups. Monitor and close them so that the program can continue{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}A good sign will be that the red Xs matches the green dots that are the vertices. If they dont match at all, that is a bad sign.{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}When its bad, you could retake another set of calibration images, or just re-run because sometimes it resolves itself.{Style.RESET_ALL}")
    answer = 0
    while answer != 'y' and answer != 'n':
        answer = input(f"{Fore.LIGHTRED_EX}Do you want to calibrate the camera? (y/n) {Style.RESET_ALL}")

    if (answer == 'y'):
        calibrate_camera(vtx_short, vtx_long, calib_sq, './CalibrationImages/*.jpg')

    poly_incident_angle_to_radius, principal_point, estimated_fov = import_camera_intrinsic_function()

    image, im_height, im_width = read_image_file()

    direct_irradiance, diffuse_irradiance, time_array = retrieve_PVGIS_irradiance(lat, long, st_year, ed_year, inclination=incline, orientation=orient)

    astropy_coords = sunpath_from_astropy(lat, long, elev, time_array)

    compensated_diffuse = compensate_diffuse_irradiance(image, diffuse_irradiance, poly_incident_angle_to_radius, principal_point, estimated_fov, im_height, im_width)

    compensated_direct = compensate_direct_irradiance(image, im_height, im_width, poly_incident_angle_to_radius, principal_point, orient, incline, estimated_fov, astropy_coords, direct_irradiance, time_array)

    final_irradiance = compensated_direct + compensated_diffuse

    state_of_charge_estimation(final_irradiance, time_array, solar_peak, conv_eff, charge_eff, discharge_eff, max_soc, min_soc, batt_nom_cap, batt_nom_volt)

    # plt.plot(time_array, final_irradiance)
    # plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # lat, long, elev, orient, incline, vtx_short, vtx_long, calib_sq, st_year, ed_year, solar_peak, conv_eff, charge_eff, discharge_eff, max_soc, min_soc = read_user_data()
    irradianceForecast()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
