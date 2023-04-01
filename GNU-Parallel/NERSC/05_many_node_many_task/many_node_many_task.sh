#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=2
#SBATCH --constraint=cpu
#SBATCH --ntasks-per-node 1

srun --no-kill --ntasks=2 --wait=0 driver.sh $1 
