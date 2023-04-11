# Balsam on Perlmutter

## Setup Balsam site

In terminal log into balsam and create your site in a folder of your choosing:
```bash
balsam login
balsam site init -n perlmutter_tutorial perlmutter_tutorial
```

Now start the site:
```bash
cd perlmutter_tutorial
balsam site start
cd ..
```

## How to run the tutorial

Follow the tutorial either with the scripts or with the jupyter notebook [notebook](balsam_tutorial.ipynb).

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
