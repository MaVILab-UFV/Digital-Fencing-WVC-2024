# Digital Fencing for Farms: Enhancing Object Detection through Multi-Dataset Integration

Welcome to the repository for our paper “Digital Fencing for Farms: Enhancing Object Detection through Multi-Dataset Integration”, accepted at XIX Workshop de Visão Computacional (WVC), 2024.

[![Overview of our method](overview.png)]

> Overview of our method, which is divided into three steps. The first step involves data preparation, where image datasets are selected, and their annotations are converted to a unified format (YOLO format). These images and annotations are then merged into a single dataset. In the second step, subsets of data and classes (SmartClass) are created to ensure consistent class annotations. Finally, in the third step, models are trained using the YOLOv8 architecture with transfer learning.

If you find this work useful for your research, please cite our paper:

```bibtex
@inproceedings{Ferreira2024,
    title        = {Digital Fencing for Farms: Enhancing Object Detection through Multi-Dataset Integration},
    author       = {Ferreira, Juliana Quintiliano and Silva, Lucas and Gomes, Thiago L. and Silva, Michel Melo},
    year         = 2024,
    booktitle    = {Proceedings of the XIX Workshop de Visão Computacional (WVC)},
    organization = {WVC},
    url          = {}
}

```

## Contact

### Authors

| [Juliana Quintiliano Ferreira](https://github.com/JulianaQuintiliano) | [Lucas Silva](https://github.com/Lucas-silva23) | [Thiago L. Gomes](https://github.com/thiagoluange) | [Michel Melo Silva](https://michelmelosilva.github.io/) |
| :---------------------------------------------------------------: | :------------------------------------------: | :-----------------------------------------------: | :--------------------------------------------------: |
|                              MSc. Student¹                        |                 BSc. Student¹                |                Assistant Professor¹               |                Assistant Professor¹                   |
|               <juliana.q.ferreira@ufv.br>                         |           <lucas.silva23@ufv.br>             |           <thiago.luange@ufv.br>                  |           <michel.m.silva@ufv.br>                    |

¹Universidade Federal de Viçosa  
Departamento de Informática  
Viçosa, Minas Gerais, Brazil



### Laboratory

| [<img src="https://raw.githubusercontent.com/MaVILab-UFV/mavilab-ufv.github.io/main/images/mavilab-logo.svg" height="300" alt="MaVILab" />](https://mavilab-ufv.github.io/) | [<img src="ufv.png" height="300" alt="UFV" />](https://www.ufv.br/) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |

**MaVILab**: Machine Vision and Intelligence Laboratory \
 <https://mavilab-ufv.github.io>

## Acknowledgements

We would like to thank CAPES, CNPq and FAPEMIG, for supporting this project.