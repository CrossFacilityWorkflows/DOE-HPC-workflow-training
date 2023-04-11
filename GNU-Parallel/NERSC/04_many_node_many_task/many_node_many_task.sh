#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=2
#SBATCH --constraint=cpu
#SBATCH --ntasks-per-node 1

srun --no-kill --ntasks-per-node=1 --wait=0 driver.sh $1 
