#!/bin/bash
#
#-  summit-setup.bash ~~
#

# Conda environment creation and installation (commented out but good to know
# later what you did!)

export DEMO_DIR=${PROJWORK}/stf019/test-fireworks

#module load gcc
#module load python
#conda create -p ${DEMO_DIR}/conda-stuff
source activate ${DEMO_DIR}/conda-stuff
#conda install -c conda-forge \
#   fireworks numpy pandas pytest scikit-learn
#MPICC="mpicc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py

# Export MongoDB connection string as environment variable to be imported into
# Python programs.
export MONGODB_URI="mongodb://admin:password@apps.marble.ccs.ornl.gov:30068/test?authSource=admin"

#-  vim:set syntax=sh:

#-  vim:set syntax=sh:
