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

def median_function(matrix,ksize,flag=None):
    normalv = matrix
    ksizev = ksize
    shape = matrix.shape

    if ksizev %2 != 0 and len(shape) >= 2:
        try:
            return cv.medianBlur(matrix.astype('uint8'),ksizev)
            print(normal.dtype)
        except Exception as kernel_size_exception:
            try:
                return cv.medianBlur(matrix.astype('uint8'),ksizev)
                print(normal.dtype)

            except Exception as kernel_size_exception2:
                print(ksizev,shape,kernel_size_exception,kernel_size_exception2)
    
    else:
        return None


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

def tumor_detection_function(matrix):
    
    try:
        normal_image = matrix
        image = matrix
        channel = None

        if len(image.shape) == 3:
            image = image[:,:,1]

        normalized_matrix = (image - np.min(image)) / (np.max(image) - np.min(image))

        thresholded = filters.threshold_otsu(normalized_matrix)
        binary_mask = normalized_matrix > thresholded

        clean = morphology.remove_small_objects(binary_mask,100)
        clean = morphology.binary_closing(clean,morphology.disk(4))

        label = measure.label(clean)
        regionprops = measure.regionprops(label)

        if regionprops:
            large_objects = max(regionprops, key=lambda r :r.area)
            tumor_mask = label == large_objects.label
            
        else:
            tumor_mask = np.zeros_like([])

        if len(image.shape) == 1 or len(image.shape) == 2:
            overlay = np.dstack([normal_image]*1)
            overlay[tumor_mask] = [1] #burası tümörlü  yeri gösteriyormu yoksa tümörsüz yeri mi gösteriyor emin değilim  
            return overlay
        
        else:
            tumor_mask = filters.sobel(tumor_mask)
            overlay = np.dstack([normal_image]*3)
            overlay[tumor_mask] = [0,128,0]

            return overlay
    except:
        print(image.shape)

def mrı_slice_returner(dat,h,w,d,val):
    matrix = dat

    if val == d - 2:
        val = d - 2
    
    else:
        pass

    image = dat[:,:,val]

    return h,w,d,image
