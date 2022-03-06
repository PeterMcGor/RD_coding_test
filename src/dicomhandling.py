#!/usr/bin/python3  
# -*- coding: utf-8 -*
#----------------------------------------------------------------------------
# Created By: Pedro Macías Gordaliza
# Created Date: 6/3/2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" 
This module implements the classes DcmFilter and DcmRotate, the function
check_ipp and needed auxiliary functionsto accomplish objectives 1-5 described 
in the R&D document.

TO COMPLETE

Design decisions: Generally, medical images cannot be understood as simple 
multidimensional arrays (i.e., tensors). The transformations performed on them
must consider the image's metadata (e.g., spacing, origin, direction).
However, the transformations requested in the R&D document of this test point 
to the handling of NumPy arrays. Therefore, to meet requirement 4: "Efficient 
implementation of these classes will be positively evaluated." 
the transformations (filtering and rotation) are done using libraries designed
for the handling of such arrays, NumPy itself and scipy.
However, to facilitate the possible extensibility of the module, 
I introduce SimpleITK, the python-wrapped version of the ITK (https://itk.org/),
designed for handling medical images. 
Its use in this version is limited to reading images as 2D axial slices and the
DICOM metadata, as well as saving images in "jpg" format.

Besides, to build and maintain a cleaner architecture type hints are employed    
""" 

from typing import Union

import sys
import os
import glob
import numpy as np
import SimpleITK as sitk

from scipy.ndimage import gaussian_filter


# 0020|0032 is the DICOM tag for ImagePatientPosition
# https://dicom.innolitics.com/ciods/rt-dose/image-plane/00200032
IPP_TAG = '0020|0032' 


def save_array_as_jpg(image_arr:np.array, path:str):
    """
    Images are stored employing SimpleITK. 
    Since jpg format requires 8-bit codification per voxel (i.e., 0-255 pixel values)
    the images are rescaled first to avoid saturation and subsequenly cast to unsigned integer 
    """
    path = path if path.endswith('.jpg') else path+'.jpg'
    itk_image = sitk.GetImageFromArray(image_arr)
    if itk_image.GetPixelIDValue != sitk.sitkUInt8:
        itk_image = sitk.Cast(sitk.RescaleIntensity(itk_image, outputMinimum=0, outputMaximum=255), sitk.sitkUInt8)
    sitk.WriteImage(itk_image, path)

def get_dcm_metadata(itk_image:sitk.Image) -> dict:
    """
    Extract the metadata cotained in a DICOM file as a dictionary
    Parameters
    ----------
    itk_image : image object with dicom metadata

    Returns
    -------
        A python dict with dicom tags as keys. 
    """
    return {tag:itk_image.GetMetaData(tag) for tag in itk_image.GetMetaDataKeys()}

def _check_path_file(path:str)->str:
    assert os.path.exists(path), path+" does not exists"
    return path

def _get_dcm_itk_img(path:str)->(np.array, dict):
    """
    Checks if the image path exists and if the provided image accomplishes with the DICOM format.
    If the image is correct the SimpleITK auxiliary functions transforms the itk image object in the example require numpy array
    Besides, return all the DICOM metadata. This approach enables future extensions for which meaningful
    information could be essential (e.g., spacing, origin).   
    """
    path = _check_path_file(path)
    itk_img = sitk.ReadImage(path)
    assert len(itk_img.GetMetaDataKeys()) > 0, "The image is not a DICOM or there is not metadata"
    #This example employs 2D images so the last dimension is squeezed. 
    #Note that by just changing this function the implementation is extensible to higher dimensional images
    return (sitk.GetArrayFromImage(itk_img[:,:,0]), get_dcm_metadata(itk_img))

def _get_ipp(dcm_metadata:dict, sep = "\\")->list:
    return [float(ax.strip()) for ax in dcm_metadata[IPP_TAG].split(sep)]



class DcmFilter:
    """
    DcmFilter implementation. 
    Parameters
    ----------
    path : Path to a dicom image
    sigma : Standard deviation for the gaussian kernel

    Returns
    -------
        Dcm Filter object with .....
    """
    def __init__(self, path:str, sigma:float = 3.0):
        self.original = path
        self.filtered = sigma
        #the ipp is setted once is checked the existence of DICOM information
        
    @property
    def original(self):
        return self._original
    
    @original.setter
    def original(self, path:str):
        self._original, dcm_metadata = _get_dcm_itk_img(path)
        # ipp will be updated with the original image
        self.ipp = dcm_metadata
        
    @property
    def filtered(self):
        return self._filtered
    @filtered.setter
    def filtered(self, sigma:float):
        self._filtered = gaussian_filter(self.original,sigma=sigma)
        
    @property
    def ipp(self):
        return self._ipp
    
    @ipp.setter
    def ipp(self, dcm_metadata:dict):
        self._ipp = _get_ipp(dcm_metadata)
        
        

class DcmRotate:
    """
    DcmRotate implementation. 
    Parameters
    ----------
    path : Path to a dicom image
    angle : Rotation angle in degrees. Must be a multiples of 90°

    Returns
    -------
        DcmRotate object with .....
    """
    def __init__(self, path:str, angle:int = 180):
        self.original = path
        self.rotated = angle
        #the ipp is setted once is checked the existence of DICOM information
        
    @property
    def original(self):
        return self._original
    
    @original.setter
    def original(self, path:str):
        self._original, dcm_metadata = _get_dcm_itk_img(path)
        # ipp will be updated with the original image
        self.ipp = dcm_metadata
        
    @property
    def rotated(self):
        return self._rotated
    
    @rotated.setter
    def rotated(self, angle:int):
        assert angle/90 == angle//90, 'The roatation angle is not a multiple of 90°'
        self._rotated = np.rot90(self.original, angle//90)
        
            
    @property
    def ipp(self):
        return self._ipp
    
    @ipp.setter
    def ipp(self, dcm_metadata:dict):
        self._ipp = _get_ipp(dcm_metadata)
        

def check_ipp(dcm_obj1:Union[DcmFilter, DcmRotate], dcm_obj2:Union[DcmFilter, DcmRotate]):
    return dcm_obj1.ipp == dcm_obj2.ipp
