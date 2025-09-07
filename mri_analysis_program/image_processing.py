from skimage import filters,morphology,measure
import cv2 as cv
import numpy as np

def to_matrix(image):
    try:
        return cv.imread(image)
    except:
        print('image_path or name:', f'{image}')

def threshold_function(matrix,thres,maxval,flag):
    if flag == 'binary':
        return cv.threshold(matrix,thres,maxval,cv.THRESH_BINARY)
    
