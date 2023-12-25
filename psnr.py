import cv2
from math import log10, sqrt 
import numpy as np

def PSNR(original, compressed):
    # Resize images to a common size
    # rHeight = 256
    # rWidth = 256

    # Resize images for first image
    # firstI = cv2.resize(original, (rWidth, rHeight))
    # Resize the details for second image
    # secondI = cv2.resize(compressed, (rWidth, rHeight))

    mse = np.mean((original - compressed) ** 2) 
    if(mse == 0):  # MSE is zero means no noise is present in the signal . 
                  # Therefore PSNR have no importance. 
        return 100
    max_pixel = 255.0
    psnr_score = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr_score 