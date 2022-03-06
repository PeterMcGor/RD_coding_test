from dicomhandling import DcmFilter, DcmRotate, check_ipp, save_array_as_jpg

if __name__ == '__main__':
    ## Simple test for DcmFilter ###
    path = '../T1_3D_TFE - 301/IM-0001-0035-0001.dcm'
    sigma = 5
    dcm_filter = DcmFilter(path, sigma)
    print(dcm_filter.original.shape)
    print(dcm_filter.filtered.shape)
    print(dcm_filter.ipp)
    save_array_as_jpg(dcm_filter.original, './ori')
    save_array_as_jpg(dcm_filter.filtered, './filt.jpg')
    ## Simple test for DcmRotate ###
    path2 = '../T1_3D_TFE - 301/IM-0001-0086-0001.dcm' 
    angle = 270
    dcm_rotate = DcmRotate(path2, angle)
    print(dcm_rotate.original.shape)
    print(dcm_rotate.ipp)
    save_array_as_jpg(dcm_rotate.original, './ori2')
    save_array_as_jpg(dcm_rotate.rotated, './rot.jpg')
    
    ## Simple test for check_ipp ###
    print("Same", check_ipp(dcm_filter, dcm_filter))
    print("Different", check_ipp(dcm_filter, dcm_rotate))