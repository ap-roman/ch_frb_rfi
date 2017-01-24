# This file contains RFI transform chains for CHIME!
# Most functions here return lists of rf_pipelines.wi_transform objects.

import os
import sys
import glob
import rf_pipelines


class new_transform(rf_pipelines.py_wi_transform):
    def __init__(self):
        pass


def detrender_chain(ix, detrend_nt=2048, cpp=True):
    return [ rf_pipelines.polynomial_detrender(deg=4, axis=1, nt_chunk=detrend_nt, cpp=cpp),
             rf_pipelines.polynomial_detrender(deg=8, axis=0, nt_chunk=detrend_nt, cpp=cpp),
             rf_pipelines.plotter_transform('dc_out%d' % ix , img_nfreq=512, img_nt=1200, downsample_nt=16) 
           ]


def clipper_chain(jx, ix, two_pass=True, clip_nt=1024, cpp=True):
    if (ix == 0) and (two_pass is True):
        pass
    else:
        two_pass = False

    return [ rf_pipelines.intensity_clipper(sigma=3, niter=12, iter_sigma=3, axis=None, nt_chunk=clip_nt, Df=2, Dt=16, cpp=cpp),
             rf_pipelines.intensity_clipper(sigma=3, niter=1, iter_sigma=3, axis=0, nt_chunk=clip_nt, Df=1, Dt=1, cpp=cpp),
             rf_pipelines.intensity_clipper(sigma=3, niter=1, iter_sigma=3, axis=1, nt_chunk=clip_nt, Df=1, Dt=1, two_pass=two_pass, cpp=cpp),
             rf_pipelines.std_dev_clipper(sigma=3, axis=1, Dt=16, two_pass=two_pass, cpp=cpp)
           ]


def transform_chain(detrender_niter=2, clipper_niter=3, detrend_nt=2048, clip_nt=1024, two_pass=True, cpp=True):
    transform_chain = [ rf_pipelines.plotter_transform('raw', img_nfreq=512, img_nt=1200, downsample_nt=16),
                        rf_pipelines.badchannel_mask('/data/pathfinder/rfi_masks/rfi_20160705.dat', nt_chunk=clip_nt)
                      ]

    for ix in xrange(detrender_niter):
        for jx in xrange(clipper_niter):
            transform_chain += clipper_chain(jx, ix, two_pass=two_pass, clip_nt=clip_nt, cpp=cpp)
        transform_chain += detrender_chain(ix, detrend_nt=detrend_nt, cpp=cpp)

    return transform_chain
