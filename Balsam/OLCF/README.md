# Balsam on Summit

## Installation

You will need to work out of a directory to which Summit's compute nodes can read and write (for example, within $PROJWORK but not $HOME). For more information, see this page. Here, we use $DEMO_DIR as a convention.

```bash
$ export DEMO_DIR="${PROJWORK}/stf019/balsam-demo" # Note: change project ID
$ module load gcc
$ module load python
$ conda create -p ${DEMO_DIR}/conda-stuff-balsam
$ source activate ${DEMO_DIR}/conda-stuff-balsam
$ pip install --pre balsam
$ pip install numpy scipy matplotlib jupyterlab jupyterlab_spellchecker
```

## Setup Balsam site

In a terminal on Summit, log into balsam and create your site:
```bash
balsam login
balsam site init -n summit_tutorial summit_tutorial
```

Now start the site:
```bash
cd summit_tutorial
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

To open the notebook follow the instructions for your site below (you can also run the notebook locally):

Create an ssh tunnel:

step 1: (From your local computer)
```bash
ssh -L 9900:localhost:9900 csimpson@summit.alcf.anl.gov
```

step 2:
```bash
jupyter notebook --no-browser --port 9900
```

step 3: Open browser on local computer and go to http://localhost:9900/?token=xxxxx

You will likely need to replace 9900 with a different number so as to not select the same port as another workshop participant running this demo.  You can choose any number between 9000 and 65535.

