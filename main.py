# This is a sample Python script.

import camera_coords_to_image_intrinsic as intrinsic
import astropy_to_camera_extrinsic as extrinsic
import import_camera_intrinsic_function as import_cam_model
import compute_diffuse_shading_factor as diffuse
import read_image_file as read_im
import numpy as np


def print_hi(name):
    poly_incident_angle_to_radius, principal_point, estimated_fov = import_cam_model.import_camera_intrinsic_function()
    #
    # # Use a breakpoint in the code line below to debug your script.
    # camera_homo_coords = extrinsic.astropy_to_camera_extrinsic([np.array([30,60]),np.array([60,30])], 20, 10)
    # image_coords = intrinsic.camera_coords_to_image_intrinsic(camera_homo_coords, poly_incident_angle_to_radius, principal_point)
    # print(image_coords)
    image = read_im.read_image_file()
    diffuse.compute_diffuse_shading_factor(image, [100,200,300,400], poly_incident_angle_to_radius, principal_point, estimated_fov)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
