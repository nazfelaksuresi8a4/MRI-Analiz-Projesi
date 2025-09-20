from skimage import filters,morphology,measure
import cv2 as cv
import nibabel as nib   
import numpy as np
import matplotlib.pyplot as plt

def take_image_obj(path):
    real_path = path
    image_object = None

    if str(real_path).endswith('.nii'):
        pass
    
    else:
        img = cv.imread(real_path,cv.IMREAD_GRAYSCALE)
    
        image_object = img
    
    return image_object

def masking(matrix):
    real_matrix = matrix

    normalize_matrix = (real_matrix - np.min(real_matrix)) / (np.max(real_matrix) - np.min(real_matrix))

    threshold = filters.threshold_otsu(normalize_matrix)
    binary_mask = normalize_matrix > threshold

    clean = morphology.remove_small_objects(binary_mask,min_size=100)
    clean = morphology.binary_closing(clean,morphology.disk(100))

    labeled = measure.label(clean)
    regions = measure.regionprops(labeled)

    if regions:
        largest_pixels = max(regions,key=lambda r : r.area)
        tumor_mask = labeled == largest_pixels.label
    
    else:
        tumor_mask = np.zeros_like([])

    overlay = np.dstack([normalize_matrix]*3)
    overlay[tumor_mask] = [0,128,0]

    return (tumor_mask,overlay,real_matrix)

f1 = take_image_obj(r'C:\Users\alper\Desktop\testing_zone\MRI_of_Human_Brain.jpg')
mri_mask,masked_mri,matrix = masking(f1)

fig,ax = plt.subplots(nrows=2,ncols=1,figsize=(5,4))

ax[0].imshow(mri_mask,cmap='gray')
ax[1].imshow(masked_mri,cmap='gray')

plt.show()