# Balsam on Cori

This tutorial will show you how to setup a Balsam site and run simulations via Balsam on Cori. For this tutorial we are using the application `LAMMPS`, a large scale classical molecular dynamics code that stands for Large-scale Atomic/Molecular Massively Parallel Simulator. 

## Installation

To setup the tutorial environment run the following command in a shell on Cori:
```bash
source setup.sh --site NERSC
```

## Setup Balsam site

In a shell on Cori, log into balsam and create your site:
```bash
balsam login
balsam site init -n cori_tutorial cori_tutorial
```

Now start the site:
```bash
cd cori_tutorial
balsam site start
cd ..
```

## How to run the tutorial

Follow the tutorial either with the scripts or with the jupyter [notebook](balsam_tutorial.ipynb).

### Scripts

To execute the scripts, run them in order as we progress:

```python 
python 0_application.py
python 1_define_jobs.py
python 2_submit_jobs.py
python 3_plot_results.py
```

### Notebook

Use NERSC's Jupyter Hub to open the notebook by following this link https://jupyter.nersc.gov/. 
