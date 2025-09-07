from skimage import filters,morphology,measure
import cv2 as cv
import numpy as np

def to_matrix(image):
    try:
        return cv.imread(image)
    except:
        print('image_path or name:', f'{image}')

def threshold_function(matrix,thres,maxval,flag):
    normal = matrix

    if flag == 'binary':
        thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_BINARY)

        return (matlike,normal)

    elif flag == 'binary_inv':
        thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_BINARY_INV)

        return (matlike,normal)
    
    elif flag == 'threshold_trunc':
        thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TRUNC)

        return (matlike,normal)

    elif flag == 'threshold_tozero':
        thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TOZERO)

        return (matlike,normal)

    elif flag == 'threshold_tozero_inv':
        thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TOZERO_INV)

        return (matlike,normal)

def gaussian_function(matrix,kszie,sigmax,sigmay):
    normal = matrix

    ksizev = kszie
    sigmaxv = sigmax
    sigmayv = sigmay
    
    k1,k2 = ksizev

    if k1 %2 != 0 and k2 %2 != 0:
        gaussian = cv.GaussianBlur(normal,ksizev,sigmaxv,sigmayv)

        return (gaussian,normal)

def sobel_function(matrix):
    normal_matrix = matrix 

    shape_tuple = normal_matrix.shape

    if len(shape_tuple) == 3:
        two_channel_matrix = cv.cvtColor(normal_matrix,cv.COLOR_BGR2GRAY)
        sobel_matrix = filters.sobel(two_channel_matrix)

        return (sobel_matrix,normal_matrix)
    
    elif len(shape_tuple) == 2:
        sobel_matrix = filters.sobel(normal_matrix)
        return (sobel_matrix,normal_matrix)
    
    else:
        print('hata: Bilinmeyen dosya!')

        return [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]]