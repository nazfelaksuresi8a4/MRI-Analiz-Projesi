from skimage import filters,morphology,measure
import cv2 as cv
import numpy as np
import winsound as ws   
from tkinter import messagebox

def to_matrix(image):
    try:
        return cv.imread(image)
    except:
        print('image_path or name:', f'{image}')

def threshold_function(matrix,thres,maxval,flag):
    normal = matrix
    try:
        if flag == 'binary':
            thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_BINARY)

            return (matlike,normal)
        
    except Exception as thres_1_exception:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!',thres_1_exception)
        return (matlike,normal)

    try:
        if flag == 'binary_inv':
            thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_BINARY_INV)

            return (matlike,normal)
        
    except Exception as thres_2_exception:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!',thres_2_exception)
        return (matlike,normal)
    try: 
        if flag == 'threshold_trunc':
            thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TRUNC)

            return (matlike,normal)
        
    except Exception as thres_3_exception:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!',thres_3_exception)
        return (matlike,normal)
    try:
        if flag == 'threshold_tozero':
            thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TOZERO)

            return (matlike,normal)
        
    except Exception as thres_4_exception:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!',thres_4_exception)
        return (matlike,normal)
    
    try:
        if flag == 'threshold_tozero_inv':
            thres_float,matlike = cv.threshold(normal,thres,maxval,cv.THRESH_TOZERO_INV)

            return (matlike,normal)
    except Exception as thres_5_exception:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin! exception: ',thres_5_exception)
        return (matlike,normal)

def gaussian_function(matrix,kszie,sigmax,sigmay):
    normal = matrix

    ksizev = kszie
    sigmaxv = sigmax
    sigmayv = sigmay
    
    k1,k2 = ksizev

    try:
        if k1 %2 != 0 and k2 %2 != 0:
            gaussian = cv.GaussianBlur(normal,ksizev,sigmaxv,sigmayv)

            return (gaussian,normal)
    except:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!')

def median_function(matrix,ksize):
    normalv = matrix
    ksizev = ksize
    shape = matrix.shape

    if ksizev %2 != 0 and len(shape) %2 != 0:
        return cv.medianBlur(matrix,ksizev)

    else:
        return 'image_processing_failure'

def blur_function(matrix,value):
    normalv = matrix
    valuev = value
    
    return cv.blur(matrix,valuev)

def sobel_function(matrix):
    normal_matrix = matrix 

    shape_tuple = normal_matrix.shape

    try:
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
    except:
        ws.Beep(1000,500)
        messagebox.showerror('HATA!','Lütfen Bir dosya tanımlayıp tekrar deneyin!')