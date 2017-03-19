# This module defines CHIME FRB acquisitions on frb1.mcgill.physics.ca
# Most functions here return rf_pipelines.wi_stream objects.

import os
import glob
import rf_pipelines


def toy():
    """A small arbitrarily-chosen acquisition that we like to use for testing. (1K freq)"""

    filename_list = [ '00000327.h5', '00000344.h5' ]
    filename_list = [ os.path.join('/data/pathfinder/16-09-19-incoherent-without-noise-source',f) for f in filename_list ]

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def small():
    """A small arbitrarily-chosen acquisition for testing, a little larger than toy(). (1K freq)"""

    basename_list = [ '00000327.h5', '00000344.h5', '00000360.h5', '00000376.h5', '00000393.h5', '00000409.h5',
                      '00000426.h5', '00000442.h5', '00000458.h5', '00000475.h5', '00000491.h5', '00000508.h5',
                      '00000524.h5', '00000540.h5', '00000557.h5', '00000573.h5', '00000589.h5', '00000606.h5',
                      '00000622.h5', '00000639.h5', '00000655.h5', '00000671.h5', '00000688.h5' ]

    acqdir = '/data/pathfinder/16-09-19-incoherent-without-noise-source'
    filename_list = [ os.path.join(acqdir, basename) for basename in basename_list ]

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def incoherent_16_09_19():
    """This is a large acquisition! (~50 GB, 1K freq)"""

    # Noise source was turned off in this acquisition, so no 'noise_source_align' argument here.
    return rf_pipelines.chime_stream_from_acqdir('/data/pathfinder/16-09-19-incoherent-without-noise-source')


def baseband_26m_b1937_16_04_22_1K():
    """A small sample of 1K-frequency data from the 26m telescope"""

    return rf_pipelines.chime_stream_from_acqdir('/data2/baseband_26m_b1937_16_04_22/1k')


def baseband_26m_b1937_16_04_22():
    """Baseband 26m data with 16K upchannelization"""
    
    return rf_pipelines.chime_stream_from_acqdir('/data2/baseband_26m_b1937_16_04_22')


def sample(path, start, end):
    """A handy function which allows user to select a range of files from an input path"""

    filename_list = sorted(glob.glob(path))[start:end]
    return rf_pipelines.chime_stream_from_filename_list(filename_list, nt_chunk=1024)


def ex_pulsar_search0():
    """Example: a pulsar in an incoherent-beam acquisition (1K freq)"""

    return rf_pipelines.chime_stream_from_times('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0', 143897.510543, 144112.258908)


def ex_storm_0b():
    """Example: an RFI storm in an incoherent-beam acquisition (1K freq)"""

    return rf_pipelines.chime_stream_from_times('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_0b', 87586.4627610, 88359.5568742)


def ex_storm_1c():
    """Example: an intense RFI storm in an incoherent-beam acquisition (1K freq)"""

    return rf_pipelines.chime_stream_from_times('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_1c', 117974.363013, 118103.212032)


######################################## INCOHERENT-BEAM DATA AVALANCHE ########################################

def incoherent_search0():
    """A large acquisition in 1K freq channels (~45 hours of data!)"""

    return rf_pipelines.chime_stream_from_acqdir('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_0')


def incoherent_search1():
    """A large acquisition in 1K freq channels (~21 hours of data!)"""

    return rf_pipelines.chime_stream_from_acqdir('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_search_1')


def incoherent_1c():
    """A large acquisition in 1K freq channels (~44 hours of data!)"""

    return rf_pipelines.chime_stream_from_acqdir('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_1c')


def incoherent_1d():
    """The first 60 hours of a very large acquisition in 1K freq channels"""

    return sample('/data2/17-02-08-incoherent-data-avalanche/frb_incoherent_1d/*.h5', 0, 10000)
