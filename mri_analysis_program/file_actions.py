import nibabel as nib
import pydicom as pydcm

def matrix_returner(path,name):
    if str(path).endswith('.nii'):
        if type(name) == type('str') or type(name) == type('str'):
                try:
                    string_path = str(path)

                    nib_file = nib.load(string_path)

                    fdata = nib_file.get_data()
                    
                    h,w,d = fdata.shape

                    return fdata,h,w,d
                except Exception as matrix_exception:
                    try:
                        string_path = str(path)

                        nib_file = nib.load(string_path)

                        fdata = nib_file.get_data()
                        
                        h,w,d = fdata.shape

                        return fdata,h,w,d
                    except:
                        print(matrix_exception,'m1-file_actions')

    elif str(path).endswith('.nii.gz'):
        if type(path) == type('str') or type(path) == type('str'):
                try:
                    string_path = str(path)

                    nib_file = nib.load(string_path)

                    fdata = nib_file.get_fdata()

                    fdata.astype('float32')

                    metashape = fdata.shape
                    if len(metashape) == 3:
                        h,w,d = metashape

                        print(fdata,h,w,d)
                        return (fdata,h,w,d) 

                    elif len(metashape) == 4:
                        h1,h2,w,d = metashape

                        print(fdata,h1,h2,w,d)
                        return (fdata,h1,h2,w,d)

                except Exception as matrix_exception:
                    print(matrix_exception)
                    print('MRI-matrix-returner-2')

                
