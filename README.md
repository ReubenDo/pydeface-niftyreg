

# PyDeface-Niftyreg
A tool to remove facial structure from MRI images.

If you find this code useful for your research, please cite the following paper:

```
@article{juvekar2024remind,
  title={{ReMIND: The Brain Resection Multimodal Imaging Database},
  author={Juvekar, Parikshit and Dorent, Reuben and K{\"o}gl, Fryderyk and Torio, Erickson and Barr, Colton and Rigolo, Laura and Galvin, Colin and Jowkar, Nick and Kazi, Anees and Haouchine, Nazim and others},
  journal={Scientific Data},
  volume={11},
  number={1},
  pages={494},
  year={2024},
  publisher={Nature Publishing Group UK London}
}
```

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
