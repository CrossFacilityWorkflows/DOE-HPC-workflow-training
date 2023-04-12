#!/bin/bash

for ENVS in $(env | grep CONDA | cut -d'=' -f1); do echo $ENVS; unset $ENVS; done;
module load lammps

