# Balsam Tutorial
----

## Tutorial Setup

Once you have setup your conda environment:
```bash
source setup.sh --site [local, ALCF, NERSC or OLCF]
```

Follow the tutorial via the markdown file or open the [notebook](balsam_tutorial.ipynb) at https://jupyter.nersc.gov/. You can also open the notebook on a local machine:

```bash
jupyter notebook
```


---

# Overview

This tutorial will show you how to setup a Balsam site and run simulations via Balsam. For this tutorial we are using `LAMMPS`, a large scale classical molecular dynamics code that stands for Large-scale Atomic/Molecular Massively Parallel Simulator. 

# Setup Balsam site

In terminal log into balsam and create your site in a folder of your choosing:
```bash
balsam login
balsam site init -n <site-name> <site-folder>
```

Now start the site:
```bash
cd <site-folder>
balsam site start
cd ..
```


# Create Balsam Application


```python
host_name = "perlumtter"
site_name = f"balsam_test_site_{host_name}"

```


```python
#Enter site name here
balsam_site_name = site_name
doe_site = 'NERSC'
```

We create the application using:
```shell
python application.py <site-name> <doe-center> [optional GPU=False]
```


```python
import os
from balsam.api import ApplicationDefinition

#Dict for any specific things to each machine
machine = {
    'ALCF': {'bin': 'lmp_polaris_nvhpc_kokkos'},
    'NERSC': {'bin': 'lmp'},
    'OLCF': {'bin': 'lmp_titan'}
}
GPU=True

class Lammps(ApplicationDefinition):

    site = balsam_site_name
    script_dir = os.path.abspath("")
    environment_variables = {"OMP_PROC_BIND":"spread", "OMP_PLACES":"cores"}
            
    def shell_preamble(self):
        return f'source {script_dir}/lammps_envs.sh --site {doe_site}'

    command_template = f'{machine[doe_site]["bin"]} -in lj.in'
    if GPU:
        command_template += ' -k on g {{NGPUS}} -sf kk -pk kokkos neigh half neigh/qeq full newton on'
    
    # command_template += ' -var velocity 20' #self.job.data["velocity"] #TO-DO vary the velocity with `-var`
        
    def postprocess(self):
        try:
            with open("energy.dat","r") as f:
                for line in f:
                    pass
                line_entries = line.split()
                if line_entries[0] == "1000":
                    self.job.data["final_ke"]=line_entries[1]
                    self.job.data["final_pe"]=line_entries[2]
                    self.job.data["final_temp"]=line_entries[3]
                    self.job.state="POSTPROCESSED"
                else:
                    self.job.state="FAILED"
        except:
            self.job.state="FAILED"

Lammps.sync()
```

# Create Balsam Jobs

Then we create the Balsam Jobs via this script:

```python
python define_jobs.py <site-name>
```


```python
from balsam.api import Job
import numpy as np

n_gpus = 4 if GPU else 0

velocities = np.arange(0.72,2.16,0.12)

jobs = [Job(app_id="Lammps",
            site_name=balsam_site_name,
            workdir=f"LJ/{n}",
            parameters={"NGPUS": n_gpus},
            data={"velocity":v},
            num_nodes=1,
            ranks_per_node=n_gpus,
            gpus_per_rank=1,
            threads_per_rank=8, #This sets OMP_NUM_THREADS
            launch_params={"cpu_bind":"depth"},
            tags={"parameter_test":"velocity"}
        )
        for n,v in enumerate(velocities)]

jobs = Job.objects.bulk_create(jobs)
```

# Submit Balsam Jobs

Then we submit the Balsam jobs to our site via:

```shell
python submit_jobs.py <site-name> [optional GPU=True]
```



```python
from balsam.api import BatchJob, Site

site_name = balsam_site_name
site = Site.objects.get(site_name)

BatchJob.objects.create(
    site_id=site.id,
    num_nodes=1,
    wall_time_min=30,
    job_mode="mpi",
    project="nstaff",
    queue="debug",
)
```




    BatchJob(num_nodes=1, wall_time_min=30, job_mode=mpi, optional_params={}, filter_tags={}, partitions=None, id=11833, site_id=481, scheduler_id=None, project=nstaff, queue=debug, state=pending_submission, status_info={}, start_time=None, end_time=None)




```python
for job in Job.objects.as_completed(jobs):
    print(job.workdir, job.result())

```
