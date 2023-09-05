import cv2
import sys
import os

# it checks for any image file placed in SkyImageOfSite directory
# if there are multiple files in SkyImageOfSite, it will take the first one and tell the user which one it uses
def read_image_file():
    files = os.listdir('./SkyImageOfSite')

    if (len(files) > 1):
        print('More than one file detected, therefore ', files[0], ' will be used!')

    image_to_convert = cv2.imread("./SkyImageOfSite/"+files[0], cv2.IMREAD_GRAYSCALE)

    im_height, im_width = image_to_convert.shape

    print('IMPORTANT REMINDER: the image must be in black and white!! Script DOES NOT CHECK FOR THIS.')
    print('Detected image shape H x W : ', im_height, 'px x ', im_width, 'px')

    return image_to_convert, im_height, im_width