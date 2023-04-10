#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node 1
#SBATCH -A STF019
#SBATCH -J mnmt
#SBATCH -o %x-%j.out
#SBATCH -e %x-%j.err
#SBATCH -t 00:10:00
#SBATCH -p batch

srun --no-kill --ntasks=2 --wait=0 driver.sh $1 

