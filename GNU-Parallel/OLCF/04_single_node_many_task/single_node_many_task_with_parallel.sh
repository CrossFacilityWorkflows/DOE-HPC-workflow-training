#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=00:02:00

module load parallel

srun parallel --jobs 6 ./payload.sh argument_{} :::: input.txt 
