
import omnicalib as omni
import cv2
import numpy as np
import glob
import torch
import os

from omnicalib.chessboard import get_points

def calibrate_camera(pattern_cols, pattern_rows, square_size, calibration_directory):
    # Defining the dimensions of checkerboard
    CHECKERBOARD = (pattern_cols, pattern_rows)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 2)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = []

    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    ####### THIS SECTION IS FOR OCAMCALIB PORT #######
    object_points = omni.chessboard.get_points(pattern_rows, pattern_cols, float(square_size)).view(-1, 3)
    detections = {}

    # Extracting path of individual image stored in a given directory
    images = glob.glob(calibration_directory)

    # number of images that we managed to detect the checkerboard corners
    nb_images_used_for_calib = 0

    for fname in images:
        print(fname)
        img_bw = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

        # check for 2 things: image need to be 1000x1000pixels square
        # assert img_bw.shape[0] == img_bw.shape[1], "The image need to be square"
        # assert img_bw.shape[0] == 1000, "Calibration and sky image should be 1000x1000 pixels"

        ret, corners = cv2.findChessboardCorners(img_bw, CHECKERBOARD,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret == False:
            print("Using findChessboardSB")
            ret, corners = cv2.findChessboardCornersSB(img_bw, CHECKERBOARD, cv2.CALIB_CB_EXHAUSTIVE)

        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)

            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(img_bw, corners, (11, 11), (-1, -1), criteria)

            #
            imgpoints.append(corners2)

            ####### THIS SECTION IS FOR OCAMCALIB PORT #######
            detections[fname] = {'image_points': torch.from_numpy(corners2).to(torch.float64).squeeze(1),
                                 'object_points': object_points}

            nb_images_used_for_calib = nb_images_used_for_calib + 1

        else:
            print("Failed to calibrate with this image.")

    print("Total number of images:", str(len(images)))
    print("Total images with detected checkerboards:", str(nb_images_used_for_calib))

    assert nb_images_used_for_calib >= 8, "Below 8 images used for calibration, the result would not be precise"

    # run the calibration function
    omni.main(detections, 4, 100, round(nb_images_used_for_calib / 4))

