# Balsam Tutorial
----

## Setup

Once you have setup your conda environment:
```bash
source setup.sh --site [local, ALCF, NERSC or OLCF]
```

Head to JupyterHub instance and chose the `balsam` Python kernel:
| Site | URL |
| :--- | ---: |
| ALCF | https://jupyter.alcf.anl.gov/  |
| NERSC | https://jupyter.nersc.gov/  |
| OLCF | https://jupyter.olcf.ornl.gov/ |

You can also follow the instructions below to open jupyter locally:

```bash
jupyter notebook
```

## Table of Contents

- [Part 1: Hello-World](#Part-1:-Hello-World)
- [Part 2: Multi-site Jobs](#Part-2:-Multi-site-Jobs)

---

# Part 1: Hello-World

In this part of the tutorial we will setup a Balsam site and execute a simple Python code job on the site.

## Setup Balsam site

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


## Simple Python code

Either run this code interactively via Jupyter or run `python simple_example.py --site site_name`.


```python
host_name = "perlumtter"
site_name = f"balsam_test_site_{host_name}"
```


```python
from balsam.api import ApplicationDefinition, BatchJob, Job

class VecNorm(ApplicationDefinition):
    site = site_name

    def run(self, vec):
        return sum(x**2 for x in vec)**0.5

jobs = [
    VecNorm.submit(workdir="test/1", vec=[3, 4]),
    VecNorm.submit(workdir="test/2", vec=[6, 8]),
]

BatchJob.objects.create(
    site_id=jobs[0].site_id,
    num_nodes=1,
    wall_time_min=10,
    job_mode="mpi",
    queue="debug",
    project="nstaff",
)

for job in Job.objects.as_completed(jobs):
    print(job.workdir, job.result())
```

    test/1 5.0
    test/2 10.0


---

# Part 2: Multi-site Jobs




```python

```

---
## Differences about the sites:

<details closed>
<summary>ALCF</summary>
<div>
    
```bash
module load conda
```
    
</div>
</details>
<br>

<details closed>
<summary>NERSC</summary>
<div>
    
```bash
module load python
```
    
</div>
</details>
<br>

<details closed>
<summary>OLCF</summary>
<div>
    
```bash
module load python
```
    
</div>
</details>



```python

```
