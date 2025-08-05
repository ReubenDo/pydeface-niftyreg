[![DOI](https://zenodo.org/badge/47563497.svg)](https://zenodo.org/badge/latestdoi/47563497)

# PyDeface
A tool to remove facial structure from MRI images.

## Dependencies:
- Niftyreg

## Installation
```
pip install  git+https://github.com/ReubenDo/pydeface-niftyreg#egg=pydeface-niftyreg
```

## How to use
```
pydeface Case001-preop-MR-3D_AX_T1_postcontrast.nii.gz --applyto Case001-preop-MR-3D_SAG_T2_SPACE.nii.gz --outfolder myresults
```

## License
PyDeface is licensed under [MIT license](LICENSE.txt).
