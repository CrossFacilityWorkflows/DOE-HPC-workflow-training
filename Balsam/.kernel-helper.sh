#!/bin/bash
module load MODULE_LOAD
conda activate CONDA_ENV
exec "$@"