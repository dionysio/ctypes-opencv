#!/usr/bin/env python
# ctypes-opencv - A Python wrapper for OpenCV using ctypes

# Copyright (c) 2008, Minh-Tri Pham
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#    * Neither the name of ctypes-opencv's copyright holders nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# For further inquiries, please contact Minh-Tri Pham at pmtri80@gmail.com.
# ----------------------------------------------------------------------------

from ctypes import *
from cxcore import *


#=============================================================================
# Helpers for access to images for other GUI packages
#=============================================================================

def cvImageAsString(img):
    return string_at(img[0].imageData, img[0].imageSize)
cvImageAsBuffer = cvImageAsString

# Added by Minh-Tri Pham
def cvCvMatAsBuffer(mat):
    return string_at(mat[0].data.ptr, mat[0].step * mat[0].rows)

#-----------------------------------------------------------------------------
# wx
#-----------------------------------------------------------------------------
try:
    import wx
    del(wx)

    def cvImageAsBitmap(img, flip=True):
        sz = cvGetSize(img)
        flags = CV_CVTIMG_SWAP_RB
        if flip:
            flags |= CV_CVTIMG_FLIP
        cvConvertImage(img, img, flags)
        bitmap = wx.BitmapFromBuffer(sz.width, sz.height, cvImageAsBuffer(img))
        return bitmap
except ImportError:
    pass

#-----------------------------------------------------------------------------
# numpy's ndarray -- by Minh-Tri Pham
#-----------------------------------------------------------------------------

try:
    import numpy
    del(numpy)
    
    _dict_opencvdepth2dtype = {
        IPL_DEPTH_1U: 'bool',
        IPL_DEPTH_8U: 'uint8',
        IPL_DEPTH_8S: 'int8',
        IPL_DEPTH_16U: 'uint16',
        IPL_DEPTH_16S: 'int16',
        IPL_DEPTH_32S: 'int32',
        IPL_DEPTH_32F: 'float32',
        IPL_DEPTH_64F: 'float64',
    }

    def cvIplImageAsNDarray(img):
        """Convert a POINTER(IplImage) into ndarray
        
        Input:
            img: a POINTER(IplImage)
        Output:
            img2: an ndarray
        """
        if not isinstance(img,POINTER(IplImage)):
            raise TypeError('img is not of type POINTER(IplImage)')
            
        from numpy import frombuffer, dtype
        
        dtypename = _dict_opencvdepth2dtype[img.contents.depth]
        data = frombuffer(cvImageAsBuffer(img),dtype=dtypename)
        
        w = img.contents.width
        ws = img.contents.widthStep / dtype(dtypename).itemsize
        h = img.contents.height
        nc = img.contents.nChannels

        if nc > 1:
            return data.reshape(h,ws)[:,:w*nc].reshape(h,w,nc)
        else:
            return data.reshape(h,ws)[:,:w]

    _dict_opencvmat2dtype = {
        CV_8U: 'uint8',
        CV_8S: 'int8',
        CV_16U: 'uint16',
        CV_16S: 'int16',
        CV_32S: 'int32',
        CV_32F: 'float32',
        CV_64F: 'float64',
    }

    def cvCvMatAsNDarray(mat):
        """Convert a POINTER(CvMat) into ndarray

        Input:
            mat: a POINTER(CvMat)
        Output:
            mat2: an ndarray
        """
        if not isinstance(mat,POINTER(CvMat)):
            raise TypeError('mat is not of type POINTER(CvMat)')

        from numpy import frombuffer, dtype
        
        typedepth = mat[0].type & 0x0FFF
        thetype = typedepth & ((1 << CV_CN_SHIFT)-1)
        nc = (typedepth >> CV_CN_SHIFT) + 1
        dtypename = _dict_opencvmat2dtype[thetype]
        data = frombuffer(cvCvMatAsBuffer(mat),dtype=dtypename)

        w = mat[0].cols
        ws = mat[0].step / dtype(dtypename).itemsize
        h = mat[0].rows

        if nc > 1:
            return data.reshape(h,ws)[:,:w*nc].reshape(h,w,nc)
        else:
            return data.reshape(h,ws)[:,:w]

    
    # from numpy.ctypeslib import as_array
    
    # James,

    # you can use the function PyBuffer_FromMemory or PyBuffer_FromReadWriteMemory
    # if you want to have write access to the memory space from python. I
    # use the following
    # python function:

    # def array_from_memory(pointer,shape,dtype):
        # import ctypes as C
        # import numpy as np
        # from_memory = C.pythonapi.PyBuffer_FromReadWriteMemory
        # from_memory.restype = C.py_object
        # arr = np.empty(shape=shape,dtype=dtype)
        # arr.data = from_memory(pointer,arr.nbytes)
        # return arr

    # Kilian

    
except ImportError:
    pass




#=============================================================================
# Wrap up all the functions and constants into __all__
#=============================================================================
__all__ = [x for x in locals().keys() \
    if  x.startswith('CV') or \
        x.startswith('cv') or \
        x.startswith('Cv') or \
        x.startswith('IPL') or \
        x.startswith('Ipl') or \
        x.startswith('ipl')]
