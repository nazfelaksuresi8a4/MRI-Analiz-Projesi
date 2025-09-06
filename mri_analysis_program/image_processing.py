from skimage import filters,morphology,measure
import cv2 as cv
import numpy as np

def to_matrix(image):
    try:
        return cv.imread(image)
    except:
        print('image_path or name:', f'{image}')