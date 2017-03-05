# This file contains RFI transform chains for CHIME!
# Most functions here return lists of rf_pipelines.wi_transform objects.

import os
import sys
import glob
import numpy as np
import rf_pipelines

class transform_parameters:
    """
    transform_parameters: an aggregator class to hold parameters for initializing transforms.

    Constructor syntax:

       p = transform_parameters(detrender_niter=2, clipper_niter=3, detrend_nt=2048, clip_nt=1024, cpp=True, two_pass=True, 
                                plot_type=None, plot_downsample_nt=None, plot_nxpix=None, plot_nypix=None, plot_nzoom=None,
                                bonsai_output_plot_stem=None, maskpath=None, mask=None, kfreq=1, cf_thr=1)
    
    with arguments as follows:

       - detrender_niter/clipper_niter: 
           number of iterations of outer detrender loop and inner clipper loop.

       - detrend_nt/clip_nt: 
           chunk sizes (in time samples) for detrender transforms and clipper transforms respectively.
                             
       - cpp: if True, then fast C++ transforms will be used.
              if False, then reference python transforms will be used.

       - two_pass: if True, then the first round of clipper transforms will use a
            more numerically stable, but slightly slower, clipping algorithm.

       - bonsai_output_plot_stem: if None, then no bonsai plots will be written. If a string is 
            specified (e.g. 'triggers'), then a sequence of bonsai plots will be written with 
            filenames beginning with the string (e.g. triggers_0_tree2.png).

       - bonsai_plot_nypix: is a bonsai plot argument. It specifies the number of pixels along the DM axis. 

       - maskpath: is a full path to the mask file which contains a list of previously-identified 
            RFI-contaminated frequency channels. If None, then the argument 'mask' is used instead.
        
       - mask: is a list of to-be-masked frequency channels in this format: e.g. mask=[[401,413.7],[654,736.012]]
            
       Note: If both 'mask' and 'maskpath' are None, then the badchannel_mask transform is disabled. Otherwise,
            the badchannel_mask transfrom can be appended to the transform chain via append_badchannel_mask().

       - kfreq: is a multiplicative factor for the Df argument in clipper transforms. 
            e.g., if 16K data is used, then kfreq should be 16. The default value (kfreq=1) assumes 1K frequency channels.

       - cf_thr: TODO

    The way the plotting parameters are determined deserves special explanation!

       - If the four "fine-grained" plotting parameters (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom)
         are specified explicitly, then these are used.

       - As a shortcut, one can specify the string-valued argument 'plot_type':

           plot_type='web_viewer'  shortcut for (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 256, 256, 4)
           plot_type='big'         shortcut for (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 1200, 512, 1)

       - Specifying fine-grained plotting parameters will override the plot_type defaults, e.g.
           p = ch_frb_rfi.transform_parameters(plot_type='web_viewer', plot_nzoom=6)
         gives (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) = (16, 256, 256, 6).

    By default (if no plotting-related constructor arguments are specified), plotting is disabled.
    """

    def __init__(self, detrender_niter=2, clipper_niter=3, detrend_nt=2048, clip_nt=1024, cpp=True, two_pass=True,
                 plot_type=None, plot_downsample_nt=None, plot_nxpix=None, plot_nypix=None, bonsai_plot_nypix=256, 
                 plot_nzoom=None, bonsai_output_plot_stem=None, maskpath=None, mask=None, kfreq=1, cf_thr=1):
                 

        self.detrender_niter = detrender_niter
        self.clipper_niter = clipper_niter
        self.detrend_nt = detrend_nt
        self.clip_nt = clip_nt
        self.two_pass = two_pass
        self.cpp = cpp

        self.bonsai_output_plot_stem = bonsai_output_plot_stem
        self.bonsai_plot_nypix = bonsai_plot_nypix

        self.maskpath = maskpath
        self.mask = mask

        self.kfreq = kfreq
        self.cf_thr = cf_thr

        # The rest of the constructor initializes plotting parameters.
        # See docstring above for a description of the initialization logic!

        self.make_plots = True

        if plot_type is 'big':
            self.plot_downsample_nt = 16
            self.plot_nxpix = 1200
            self.plot_nypix = 512
            self.plot_nzoom = 1
        elif plot_type is 'web_viewer':
            self.plot_downsample_nt = 16
            self.plot_nxpix = 256
            self.plot_nypix = 256
            self.plot_nzoom = 4
        elif plot_type is not None:
            raise RuntimeError("ch_frb_rfi.transform_parameters constructor: plot_type='%s' is unrecognized" % plot_type)
        elif (plot_downsample_nt is None) and (plot_nxpix is None) and (plot_nypix is None) and (plot_nzoom is not None):
            # OK: no plots will be written
            self.make_plots = False
        elif (plot_downsample_nt is None) or (plot_nxpix is None) or (plot_nypix is None) or (plot_nzoom is None):
            raise RuntimeError("transform_parameters: if plot_type is unspecified, then either all or none of"
                               + " (plot_downsample_nt, plot_nxpix, plot_nypix, plot_nzoom) must be specified")

        if plot_downsample_nt is not None:
            self.plot_downsample_nt = plot_downsample_nt
        if plot_nxpix is not None:
            self.plot_nxpix = plot_nxpix
        if plot_nypix is not None:
            self.plot_nypix = plot_nypix
        if plot_nzoom is not None:
            self.plot_nzoom = plot_nzoom

    def append_plotter_transform(self, transform_chain, img_prefix):
        if self.make_plots:
            t = rf_pipelines.plotter_transform(img_prefix, self.plot_nypix, self.plot_nxpix, self.plot_downsample_nt, self.plot_nzoom)
            transform_chain.append(t)

    def append_badchannel_mask(self, transform_chain):
        if (self.maskpath != None) or (self.mask != None):
            t = rf_pipelines.badchannel_mask(maskpath=self.maskpath, nt_chunk=self.clip_nt, mask=self.mask)
            transform_chain.append(t)

# -------------------------------------------------------------------------------------------------------

def detrender_chain(parameters, ix):
    assert isinstance(parameters, transform_parameters)

    transform_chain = [ rf_pipelines.polynomial_detrender(deg=4, axis=1, nt_chunk=parameters.detrend_nt, cpp=parameters.cpp),
                        rf_pipelines.polynomial_detrender(deg=8, axis=0, nt_chunk=parameters.detrend_nt, cpp=parameters.cpp) ]

    parameters.append_plotter_transform(transform_chain, 'dc_out%d' % ix)
    return transform_chain

def clipper_chain(parameters, ix):
    two_pass = parameters.two_pass and (ix == 0)
    
    si = 5 / parameters.cf_thr**np.log2(2*parameters.kfreq * 16)

    return [ rf_pipelines.std_dev_clipper(sigma=3, axis=1, Df=1*parameters.kfreq, Dt=16, two_pass=two_pass, cpp=parameters.cpp),

             rf_pipelines.intensity_clipper(sigma=5, niter=12, iter_sigma=si, axis=None, nt_chunk=parameters.clip_nt, Df=2*parameters.kfreq, Dt=16, cpp=parameters.cpp),
             rf_pipelines.intensity_clipper(sigma=5, niter=12, iter_sigma=si, axis=0, nt_chunk=parameters.clip_nt, Df=2*parameters.kfreq, Dt=16, cpp=parameters.cpp),
             
             rf_pipelines.intensity_clipper(sigma=5, niter=12, iter_sigma=5, axis=0, nt_chunk=parameters.clip_nt, Df=1*parameters.kfreq, Dt=1, cpp=parameters.cpp),
             rf_pipelines.intensity_clipper(sigma=5, niter=12, iter_sigma=5, axis=1, nt_chunk=parameters.clip_nt, Df=1*parameters.kfreq, Dt=1, two_pass=two_pass, cpp=parameters.cpp) ]

def transform_chain(parameters):
    transform_chain = [ ]
    parameters.append_plotter_transform(transform_chain, 'raw')
    parameters.append_badchannel_mask(transform_chain)

    for ix in xrange(parameters.detrender_niter):
        for jx in xrange(parameters.clipper_niter):
            transform_chain += clipper_chain(parameters, ix)
        transform_chain += detrender_chain(parameters, ix)

    return transform_chain
