# Balsam on Polaris

This tutorial will show you how to setup a Balsam site and run simulations via Balsam on Polaris. For this tutorial we are using the application `LAMMPS`, a large scale classical molecular dynamics code that stands for Large-scale Atomic/Molecular Massively Parallel Simulator. 

## Installation

To setup the tutorial environment run the following command in a shell on Polaris:
```bash
source setup.sh --site ALCF
```

## Setup Balsam site

In a shell on Polaris, log into balsam and create your site:
```bash
balsam login
balsam site init -n polaris_tutorial polaris_tutorial
```

Now start the site:
```bash
cd polaris_tutorial
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

To open the notebook follow these instructions to create an ssh tunnel, but replace the port number 9900 with an integer of your choice between 9000 and 65535 (it needs to be unique from other users): 

In a shell on your local machine:
```bash
ssh -L 9900:localhost:9900 csimpson@polaris.alcf.anl.gov
module load conda
conda activate balsam
jupyter notebook --no-browser --port 9900
```
The shell will generate a path that looks like http://localhost:9900/?token=xxxxx. Copy and paste it in a local browser. Navigate to your copy of the workshop repository on the file system and open the notebook.
