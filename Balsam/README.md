# Balsam

In this directory we provide instructions for running our
Balsam exercises at ALCF, NERSC, and OLCF.

This tutorial will show you how to setup a Balsam site and run simulations via Balsam. For this tutorial we are using the application `LAMMPS`, a large scale classical molecular dynamics code that stands for Large-scale Atomic/Molecular Massively Parallel Simulator. 


## Installation

To setup the tutorial environment run the following command on the site of your choice:
```bash
source setup.sh --site [local, ALCF, NERSC or OLCF]
```

## Setup Balsam site

In terminal log into balsam and create your site in a folder of your choosing:
```bash
balsam login
balsam site init -n <doe-site>_tutorial <doe-site>_tutorial
```

Now start the site:
```bash
cd <doe-site>_tutorial
balsam site start
cd ..
```

## Tutorial

Follow the tutorial via the scripts or open the [notebook](balsam_tutorial.ipynb).

### Scripts

To execute the scripts, run them in order as we progress:

```python 
python 0_application.py
python 1_define_jobs.py
python 2_submit_jobs.py
python 3_plot_results.py
```

### Notebook

To open the notebook follow the instructions for your site below (you can also run the notebook locally):

#### NERSC

Follow this link https://jupyter.nersc.gov/. 

#### OLCF and ALCF

Create an ssh tunnel:

step 1: (From your local computer)
```bash
ssh -L 9900:localhost:9900 csimpson@polaris.alcf.anl.gov
```

step 2:
```bash
jupyter notebook --no-browser --port 9900
```

step 3: Open browser on local computer and go to http://localhost:9900/?token=xxxxx

You will likely need to replace 9900 with a different number so as to not select the same port as another workshop participant running this demo.  You can choose any number between 9000 and 65535.

#### Local Machine

```bash
jupyter notebook
```
Note that if you run this notebook locally, you will need to have a copy of the LAMMPs input file and environment file on the machine where you are running LAMMPS.

