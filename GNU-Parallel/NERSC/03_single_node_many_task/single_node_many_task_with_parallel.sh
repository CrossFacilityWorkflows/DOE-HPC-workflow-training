#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --time=00:02:00

module load parallel

srun parallel --jobs 6 ./payload.sh argument_{} :::: input.txt 
