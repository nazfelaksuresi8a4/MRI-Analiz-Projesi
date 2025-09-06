import nibabel as nib
import pydicom as pydcm

#burada matrix_returner(x,y) fonksiyonunda fallback mantığı kullanıldı.

def matrix_returner(path,name):
    if path:
        if type(name) == type('str') or type(name) == str:
            if str(path).endswith('.nii'):
                try:
                    string_path = str(name)

                    nib_file = nib.load(string_path)

                    fdata = nib_file.get_fdata()
                    h,w,d = fdata.shape

                    return (fdata,h,w,d)
                except Exception as matrix_exception:
                    if path:
                        if type(path) == type('str') or type(path) == str:
                            if str(path).endswith('.nii'):
                                try:
                                    string_path = str(path)

                                    nib_file = nib.load(string_path)

                                    fdata = nib_file.get_fdata()
                                    h,w,d = fdata.shape

                                    return (fdata,h,w,d)
                                except Exception as matrix_exception:
                                    print(matrix_exception)
                                    pass

                


