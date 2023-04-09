# FireWorks demo at NERSC

We'll provide instructions for running two similar versions
of the same demo.

Demo 1- a "high throughput" version of the demo in which
every task in the workflow uses the same amount of compute
resources (2 CPU nodes).

Demo 2- a "heterogenous workflow" version of the demo
in which one task in the workflow uses more resources
than the others (1 CPU node, 2 CPU nodes, 1 CPU node).

## About the demos

We're using the open source
[Diabetes dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset)
that comes pre-installed in the `scikit-learn` package.
We'll try to determine which attribute is the greatest
risk factor for the progression of diabetes. 

- `step_1_diabetes_preprocessing.py`: we load the diabetes dataset,
  write it to two numpy .npy files
- `step_2_diabetes_correlation.py`: we load the .npy files and
  process each attribute in a separate MPI rank across 2 nodes.
  We calculate the Pearson correlation coefficient between each
  attribute and the measure of disease progression. We gather
  the outputs back to a single file.
` `step_3_diabetes_postprocessing.py`: we load the Pearson correlation
  coefficient data and pretty print it to the screen using Pandas

## Demo 1- high throughput

In this version of the demo, steps 1, 2, and 3 will all use the 
same amount of resources (2 CPU nodes). FireWorks is a bit more
natually suited to this kind of workflow and requires less configuration
so we'll start here. 

Note that step 2 deponds on step 1, and step 3 depends on step 2.

Let's start by looking at our high-throughput FireWork:

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat fw_diabetes_ht.yaml 
fws:
- fw_id: 1
  spec:
    _category: twonode
    _launch_dir: /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC  
    _tasks:
    - _fw_name: ScriptTask
      script: srun python step_1_diabetes_preprocessing.py
- fw_id: 2
  spec:
    _category: twonode
    _launch_dir: /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
    _tasks:
    - _fw_name: ScriptTask
      script: srun -n 10 --cpu-bind=cores python step_2_diabetes_correlation.py
- fw_id: 3
  spec:
    _category: twonode
    _launch_dir: /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
    _tasks:
    - _fw_name: ScriptTask
      script: srun python step_3_diabetes_postprocessing.py
links:
  1:
  - 2
  2:
  - 3
metadata: {}
```

Things to note:
- We specify the `_category` key to match our task to the right worker resources
- We specify the `_launch_dir` so that each FireWork will run in this directory.
  This is important since we are passing files between workflow steps.
- We specify the task dependencies in the `links` section

Next, let's look at our `my_fworker2.yaml`. This is the worker configuration
file that will match the `_category: twonode` key in our spec. 

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_fworker2.yaml 
name: two node fireworker
category: twonode
query: '{}'
```

Next, let's look at our `my_qadapter.yaml`. At NERSC we use a SLURM adapter- on other systems, you can
substitue the appropriate adapter.

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_qadapter.yaml
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -l /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_launchpad.yaml -w /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_fworker2.yaml singleshot
constraint: cpu
nodes: 2
ntasks: 1
account: nstaff
walltime: '00:05:00'
queue: debug
job_name: null
logdir: null
pre_rocket: null
post_rocket: null
```

Things to note:
- We unfortuatnely have to specify the full paths
  to `my_launchpad.yaml` and `my_fworker2.yaml`- bash shortcuts
  are not supported.
- We have specified `singleshot` here, since each task within the workflow only needs to run once
- We have specified the usual Slurm job resources that each task will use
  
Ok, now that we've examined all the pieces, let's run our FireWorks workflow.
Note that we are launching the workflow with `qlaunch rapidfire`. Remember that we have
specified `rlaunch singleshot` in our queue adapter- this will run each task once per job.
Howeer we need to launch 3 jobs, one for each task. For this reason we use `qlaunch rapidfire`
to automatically launch our whole workflow.

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> qlaunch rapidfire
2023-04-09 16:02:30,351 INFO getting queue adapter
2023-04-09 16:02:30,352 INFO Created new dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362
2023-04-09 16:02:30,364 INFO Launching a rocket!
2023-04-09 16:02:30,370 INFO Created new dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-02-30-369690
2023-04-09 16:02:30,370 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-02-30-369690
2023-04-09 16:02:30,372 INFO submitting queue script
2023-04-09 16:02:30,443 INFO Job submission was successful and job_id is 7199282
2023-04-09 16:02:30,443 INFO Sleeping for 5 seconds...zzz...
2023-04-09 16:02:35,452 INFO Launching a rocket!
2023-04-09 16:02:35,457 INFO Created new dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-02-35-457336
2023-04-09 16:02:35,458 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-02-35-457336
2023-04-09 16:02:35,459 INFO submitting queue script
2023-04-09 16:02:35,529 INFO Job submission was successful and job_id is 7199287
2023-04-09 16:02:35,529 INFO Sleeping for 5 seconds...zzz...
2023-04-09 16:02:40,541 INFO Finished a round of launches, sleeping for 60 secs
2023-04-09 16:03:40,601 INFO Checking for Rockets to run...
2023-04-09 16:03:40,606 INFO Launching a rocket!
2023-04-09 16:03:40,612 INFO Created new dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-03-40-611828
2023-04-09 16:03:40,612 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-03-40-611828
2023-04-09 16:03:40,614 INFO submitting queue script
2023-04-09 16:03:40,705 INFO Job submission was successful and job_id is 7199339
2023-04-09 16:03:40,705 INFO Sleeping for 5 seconds...zzz...
2023-04-09 16:03:45,717 INFO Finished a round of launches, sleeping for 60 secs
2023-04-09 16:04:45,777 INFO Checking for Rockets to run...
2023-04-09 16:04:45,782 INFO Launching a rocket!
2023-04-09 16:04:45,788 INFO Created new dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-04-45-787763
2023-04-09 16:04:45,788 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-09-23-02-30-351362/launcher_2023-04-09-23-04-45-787763
2023-04-09 16:04:45,790 INFO submitting queue script
2023-04-09 16:04:46,211 INFO Job submission was successful and job_id is 7199382
2023-04-09 16:04:46,211 INFO Sleeping for 5 seconds...zzz...
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> 
```

Notice that FireWorks actually launched 4 jobs, although we only had 3 steps in
our workflow. If a job wakes up, finds its dependencies are not yet met, it
will quit. By default FireWorks will wait 1 minute and launch another round
of jobs, which is what we saw here.

We can query the status of our workflow

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> lpad get_fws
[
    {
        "fw_id": 1,
        "created_on": "2023-04-09T22:26:05.494686",
        "updated_on": "2023-04-09T22:26:22.663317",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 2,
        "created_on": "2023-04-09T22:26:05.494797",
        "updated_on": "2023-04-09T22:27:26.764057",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 3,
        "created_on": "2023-04-09T22:26:05.494869",
        "updated_on": "2023-04-09T22:28:31.320609",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    }
]
```

FireWorks lists all of our tasks as successfully completed.

Let's take a look in our `block_<date>` directory to see what
FireWorks did. Note that in this directory, there are four
`launcher_<date>` directories that correspond to each job
that was launched in our workflow.

In our "no-op" job, the `FW_job-<jobid>.out` file includes
the message:

```
No FireWorks are ready to run and match query! {'$or': [{'spec._fworker': {'$exists': False}}, {'spec._fworker': None}, {'spec._fworker': 'two node fireworker'}], 'spec._category': 'twonode'}
2023-04-09 16:02:39,903 INFO Rocket finished
```

In the other 3 `launcher_` folders, you should see job
output in the `FW_job-<jobid>.out` files. 

Note that is is not deterministic- it depends on how busy the
queue is and how long it takes each task to run. You might
only have 3 jobs, for example. 


## Demo 2- heterogenous workflow

Let's make things a little more complicated now. 
