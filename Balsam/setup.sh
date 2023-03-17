#!/usr/bin/env bash

#=========================================
# 
# Title: setup.sh
# Author: Andrew Naylor
# Date: Mar 23
# Brief: Setup Balsam environment
#
#=========================================

## Variables
BALSAM_CONDA_ENV=balsam


## Parse Input Arg
usage() {                                 
    echo "Usage: source setup.sh --site [local, ALCF, NERSC or OLCF]" 1>&2 
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
    conda create --name $BALSAM_CONDA_ENV python=3.9 -y
    conda activate $BALSAM_CONDA_ENV
    python -m pip install -r requirements.txt
}

SITE=$2
case "$SITE" in
    local)
        if ! command -v conda &> /dev/null
        then
            echo "Error: conda required for setup"
            exit_abnormal
        fi
        ;;
    ALCF)
        module load conda
        ;;
    NERSC | OLCF)
        module load python
        ;;
    *)
        echo "Error: '$SITE' is not in the list"
        exit_abnormal
        ;;
esac

setup_general_env

## Setup Jupyter Kernel in JupyterHub
if [[ "$SITE" != "local" ]]
then
    python -m ipykernel install --user --name $BALSAM_CONDA_ENV --display-name $BALSAM_CONDA_ENV
fi
