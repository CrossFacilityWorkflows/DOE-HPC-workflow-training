# FireWorks at NERSC

First step towards creating FireWorks demo/tutorial at NERSC.

Is supposed to be a 3 part workflow, where step 1 depends on step 2 
and step 2 depends on step 3. Additionally, step 2 will use more resources
than steps 1 or 3 to run an MPI-based processing task.

The goal is to mimic the structure of a real scientific workflow,
even though the size of the dataset here is relatively small.

## Dataset

We're using the open source [Diabetes dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset)
that comes pre-installed in the `scikit-learn` package.

## Installing the environment

Note that I could not get all the depencies to resolve with Python 3.10, so 
I'm using Python 3.9. 

```
module load python
conda create -n fireworks python=3.9 -y
conda activate fireworks
conda install -c conda-forge fireworks pytest numpy scikit-learn pandas
MPICC="cc -shared" pip install --force-reinstall --no-cache-dir --no-binary=mpi4py mpi4py
```

## Known issues

Note that the different sized resources part is not yet working. I'm
working with the FireWorks developer to try to figure out how to do this.


