#!/bin/bash

if command -v conda &> /dev/null
then
    echo "deactivating conda env"
    conda deactivate
fi

module load python
module load gsl
module load cray-hdf5-parallel
module load cray-fftw
module load lammps

