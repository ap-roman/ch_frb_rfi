This directory contains a few "standard" bonsai config files that we use
when testing RFI removal.

I only put the .txt files in git, but the hdf5 files (currently needed to
create a bonsai_dedisperser, although this is a temporary kludge that will
be fixed soon I hope) can be generated with:
```
bonsai-mkweight bonsai_nfreq1024_singletree_v1.txt bonsai_nfreq1024_singletree_v1.hdf5
bonsai-mkweight bonsai_nfreq1024_3tree_v1.txt bonsai_nfreq1024_3tree_v1.hdf5
```

On frb1, the directory /data/bonsai_configs contains up-to-date copies of
these files, along with the corresponding hdf5 files.  The functions in
`ch_frb_rfi.bonsai` assume that you're running on frb1.

Current contents:

  - bonsai_nfreq1024_singletree_v1.txt

    Simplest example, intended for RFI studies with 1024-frequency data and
    testing the web viewer.  Searches with a single dedispersion tree to max DM 276.

  - bonsai_nfreq1024_3tree_v1.txt

    Slightly more complicated, also intended for RFI studies with 1024-frequency data.
    Searches with three dedispersion trees to max DM 552.

  - bonsai_nfreq16K_3tree_v1.txt

    Intended for RFI studies with 16K-frequency data.

More to come!