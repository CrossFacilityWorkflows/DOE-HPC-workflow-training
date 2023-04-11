#!/usr/bin/python3

"""
this script will read from numpy data files written in step 1
each mpi rank will select one column of the dataset for
which to compute the pearson correlation coefficient
with the disease progression metric
the goal is to calculate the correlation cofficients
of each attribute in the dataset with the final
disase progression metric

note this is way overkill for this small dataset, but the idea
is to simulate a real parallel analysis task
"""

import os
import numpy as np
from mpi4py import MPI
import socket

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Save project directory. Note the use of ${PROJWORK} -- this prevents problems
# that arise because ${HOME} is not available on Summit's compute nodes.
demo_dir = os.getenv("DEMO_DIR")

# verify we're running multinode
print("Host and rank: {hostname}, {rank}".format(
    hostname = socket.gethostname(),
    rank = rank))

# each rank should load the attribute data that we wrote in step 1
print("Loading 'x_diabetes.npy'...")
x_diabetes = np.load(os.path.join(demo_dir, "x_diabetes.npy"))

# each rank should load the disease progression measure that we wrote in step 1
print("Loading 'y_diabetes.npy'...")
y_diabetes = np.load(os.path.join(demo_dir, "y_diabetes.npy"))

# each rank should select the column for which it will compute the pearson correlation coefficient
attribute = x_diabetes[:, rank]

# compute the pearson correlation coefficient
p_corr_coeff = np.corrcoef(attribute, y_diabetes)[1][0]

# now need to collect the correlation coefficients back at rank 0 to write to a single file
all_coeffs = None
if rank == 0:
    all_coeffs = np.empty([size], dtype="float64")
comm.Gather(p_corr_coeff, all_coeffs, root=0)

# sanity check
if rank == 0:
    print(all_coeffs)

# save output file
if rank == 0:
    np.save(os.path.join(demo_dir, "all_coeffs.npy"), all_coeffs)
    print("wrote all_coeffs file")
