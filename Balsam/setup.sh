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
SITE=$2
case "$SITE" in
    local)
        if ! command -v conda &> /dev/null
        then
            echo "Error: conda required for setup"
            exit_abnormal
        fi
        conda create --name $BALSAM_CONDA_ENV python=3.9 ipykernel -y
        conda activate $BALSAM_CONDA_ENV
        python -m pip install -r requirements.txt
        ;;
    ALCF)
        module load conda
        conda create --name $BALSAM_CONDA_ENV python=3.9 ipykernel -y
        conda activate $BALSAM_CONDA_ENV
        python -m pip install -r requirements.txt
        ;;
    NERSC)
        module load python
        conda create --name $BALSAM_CONDA_ENV python=3.9 ipykernel -y
        conda activate $BALSAM_CONDA_ENV
        python -m pip install -r requirements.txt
        MODULE=python
        ;;
    OLCF)
        module load python
        conda create --name $BALSAM_CONDA_ENV python=3.9 ipykernel -y
        source activate $BALSAM_CONDA_ENV
        python -m pip install -r requirements.txt
        ;;
    *)
        echo "Error: '$SITE' is not in the list"
        exit_abnormal
        ;;
esac

## Setup Jupyter Kernel in JupyterHub
if [[ "$SITE" == "NERSC" ]]
then
    JUPYTER_KERNEL_FOLDER=$HOME/.local/share/jupyter/kernels/$BALSAM_CONDA_ENV/
    mkdir -p $JUPYTER_KERNEL_FOLDER
    cp .kernel.json $JUPYTER_KERNEL_FOLDER/kernel.json
    cp .kernel-helper.sh $JUPYTER_KERNEL_FOLDER/kernel-helper.sh
    sed -i -e "s#MODULE_LOAD#$MODULE#g" $JUPYTER_KERNEL_FOLDER/kernel-helper.sh
    sed -i -e "s#CONDA_ENV#$BALSAM_CONDA_ENV#g" $JUPYTER_KERNEL_FOLDER/kernel-helper.sh
    sed -i -e "s#CONDA_ENV#$BALSAM_CONDA_ENV#g" $JUPYTER_KERNEL_FOLDER/kernel.json
elif [[ "$SITE" == "local" ]]
then
    python -m pip install jupyter
fi
