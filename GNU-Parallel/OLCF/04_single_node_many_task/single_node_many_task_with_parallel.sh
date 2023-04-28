#!/bin/bash
#SBATCH -A STF019
#SBATCH -J payload
#SBATCH -o %x-%j.out
#SBATCH -t 00:10:00
#SBATCH -p batch
#SBATCH -N 1

module load parallel

srun parallel --jobs 6 ./payload.sh argument_{} :::: input.txt 

