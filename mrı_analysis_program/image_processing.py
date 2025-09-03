from skimage import filters,morphology,measure
import cv2 as cv
import numpy as np

def to_matrix(image):
    return cv.imread(image)