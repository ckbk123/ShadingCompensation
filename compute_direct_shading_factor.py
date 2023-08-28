import numpy as np
from tqdm import tqdm
import cv2
import camera_coords_to_image_intrinsic as intrinsic
import astropy_to_camera_extrinsic as extrinsic

def compensate_direct_irradiance(image, image_size, poly_incident_angle_to_radius, principal_point, orientation, inclination, estimated_fov, az_zen_array, direct_irradiance, original_time_array):
    print("Computing the direct shading factor...")
    direct_shading_factor = np.ones(len(direct_irradiance))

    # this section is to remove the regions where the zenith goes over the estimated fov
    combined_array = np.vstack((range(0, len(original_time_array)), az_zen_array[0], az_zen_array[1]))
    combined_array = np.delete(combined_array, np.where(combined_array[:, 2] >= estimated_fov), 1)

    # now we extract them back out to use
    index_array = combined_array[0].astype(int)
    az_array = combined_array[1]
    zen_array = combined_array[2]

    # use the extrinsic function to compute the solar homo coords in cam's reference
    camera_homo_coords = extrinsic.astropy_to_camera_extrinsic([az_array,zen_array], orientation, inclination)
    image_coords = intrinsic.camera_coords_to_image_intrinsic(camera_homo_coords, poly_incident_angle_to_radius, principal_point)

    for i in tqdm(range(1,len(index_array))):
        # This IF check for moments where we jump to the next day. It means that we should be jumping from one side of image to another, so the length of this line will be more than half of the image height
        if (np.sqrt((image_coords[i][1] - image_coords[i-1][1]) ** 2 + (image_coords[i][0] - image_coords[i-1][0]) ** 2) < image_size / 4):
            mask_im = np.zeros(shape=(image_size, image_size, 1), dtype=np.uint8)
            mask_im = cv2.line(mask_im, (image_coords[i-1][0], image_coords[i-1][1]), (image_coords[i][0], image_coords[i][1]), 255, 20)

            masked_im = cv2.bitwise_and(image, image, mask=mask_im)

            direct_shading_factor[index_array[i]] = cv2.sumElems(masked_im)[0] / cv2.sumElems(mask_im)[0]

    compensated_direct_irradiance = np.multiply(direct_irradiance, 1-direct_shading_factor)
    print("Finished compensating direct irradiance with direct shading factor")
    return compensated_direct_irradiance