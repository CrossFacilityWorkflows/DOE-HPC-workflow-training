#!/usr/bin/env bash

## Parse Input Arg
usage() {                                 
    echo "Usage: source lammps_envs.sh --site [ALCF, NERSC or OLCF]" 1>&2 
}

exit_abnormal() { 
    usage
    kill -INT $$
}

if [ $# -lt 2 ]; then
    echo "Error: script requires requires site"
    exit_abnormal
fi


## Setup environment
setup_general_env() {
    module load lammps
}

SITE=$2
case "$SITE" in
    ALCF)
        ###
        ;;
    NERSC)
        ###
        ;;
    OLCF)
        module swap PrgEnv-pgi PrgEnv-gnu
        module load fftw
        ;;
    *)
        echo "Error: '$SITE' is not in the list"
        exit_abnormal
        ;;
esac

setup_general_env

# export MPICH_GPU_SUPPORT_ENABLED=1
