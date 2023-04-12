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
  write it to two numpy `.npy` files.
- `step_2_diabetes_correlation.py`: we load the `.npy` files and
  process each attribute in a separate MPI rank across 2 nodes.
  We calculate the Pearson correlation coefficient between each
  attribute and the measure of disease progression. We gather
  the outputs back to a single file.
- `step_3_diabetes_postprocessing.py`: we load the Pearson correlation
  coefficient data and pretty print it to the screen using pandas.

## Demo 1- high throughput

In this version of the demo, steps 1, 2, and 3 will all use the 
same amount of resources (2 CPU nodes). FireWorks is a bit more
naturally suited to this kind of workflow and requires less configuration
so we'll start here. 

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

Note: you'll need to change the location of the `_launch_dir`
to your own directory.


Things to note:
- We specify the `_category` key to match our task to the right worker resources.
- We specify the `_launch_dir` so that each FireWork will run in this directory.
  This is important since we are passing files between workflow steps. Unfortunately
  we cannot use any bash shortcuts here- we have to specify the absolute path.
- We specify the task dependencies in the `links` section (2 depends on 1,
  3 depends on 2). 

Next, let's look at our `my_fworker2.yaml`. This is the worker configuration
file that will match the `_category: twonode` key in our spec. 

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_fworker2.yaml 
name: two node fireworker
category: twonode
query: '{}'
```

Next, let's look at our `my_qadapter.yaml`. At NERSC we use a Slurm adapter- on other systems, you can
substitue the [appropriate adapter](https://github.com/materialsproject/fireworks/tree/bd2bb5078122fa27a7dda2084abb3af8cac05436/fw_tutorials/queue).

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_qadapter.yaml
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -l /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_launchpad.yaml -w /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_fworker2.yaml singleshot
constraint: cpu
nodes: 2
account: nstaff
walltime: '00:05:00'
queue: debug
job_name: null
logdir: null
pre_rocket: null
post_rocket: null
```

Things to note:
- We unfortunately have to specify the full paths
  to `my_launchpad.yaml` and `my_fworker2.yaml`- bash shortcuts
  are not supported.
- We have specified `singleshot` here, since each task within the workflow only needs to run once.
- We have specified the usual Slurm job resources that each task will use.
- You'll need to modify these paths and your NERSC project account.
  
Now that we've examined all the pieces, let's run our FireWorks workflow. We are launching
this workflow from a Perlmutter login node with our `fireworks` conda environment
activated. 

Note that we will launch the workflow with `qlaunch rapidfire`. Remember that we have
specified `rlaunch singleshot` in our queue adapter- this will run each task once per job.
However we need to launch 3 jobs, one for each task. For this reason we use `qlaunch rapidfire`
to automatically launch our whole workflow. `rapidfile` will keep launching jobs until
there are no more pending FireWorks in the database.

```
lpad reset
lpad add fw_diabetes_ht.yaml
qlaunch rapidfire
```

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

Let's make things a little more complicated now. In this version of the demo,
we'll have a workflow where step 1 and step 3 only use one node, but step 2
uses two nodes.

Let's start by looking at our `fw_diabetes_wf.yaml` file

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat fw_diabetes_wf.yaml 
fws:
- fw_id: 1
  spec:
    _category: onenode
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
    _category: onenode
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

If we compare this to our `fw_diabetes_ht.yaml` file, the difference is the `_category` key.
We now have two different categories- `onenode` and `twonode`. These categories correspond
to two different FireWorker specification files `my_fworker.yaml`:

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_fworker1.yaml 
name: one node fireworker
category: onenode
query: '{}'
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_fworker2.yaml 
name: two node fireworker
category: twonode
query: '{}'
```

Note that this is the same `my_fworker2.yaml` that we used in demo 1.

Because we need to specify different sets of resources to our scheduler,
we also need to have two queue adapters- one for the `onenode` case and one
for the `twonode` case:

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_qadapter1.yaml 
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -w /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_fworker1.yaml -l /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_launchpad.yaml singleshot
constraint: cpu
nodes: 1
account: nstaff
walltime: '00:05:00'
queue: debug
job_name: null
logdir: null
pre_rocket: null
post_rocket: null
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> cat my_qadapter2.yaml 
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -w /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_fworker2.yaml -l /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/my_launchpad.yaml singleshot
constraint: cpu
nodes: 2  
account: nstaff
walltime: '00:05:00'
queue: debug
job_name: null
logdir: null
pre_rocket: null
post_rocket: null
```

Note you'll need to modify your queue adapter files to use your own files,
your own NERSC project account, etc.

We are ready to launch our heterogeneous workflow example. 

Recall that in our first example we did a
simple `qlaunch rapidfire`. We did not specify a specific queue adapter. If we do not
specify a specific queue adapter, FireWorks will chose the default file, `my_qadapter.yaml`.

However in this example, we will have to launch our workflow using both queue adapters
`my_qadapter1.yaml` and `my_qadapter2.yaml`. Note that we specify the corresponding
`my_fworker1.yaml` and `my_fworker2.yaml`, respectively, in each queue adapter
file.

To launch our workflow, we'll issue two simultaneous `qlaunch rapidfire` commands.
We are launching
this workflow from a Perlmutter login node with our `fireworks` conda environment
activated.

```
lpad reset
lpad add fw_diabetes_wf.yaml
qlaunch -q my_qadapter1.yaml rapidfire & qlaunch -q my_qadapter2.yaml rapidfire
```

If you like, you can open a second terminal to monitor the job status with
```
lpad get_fws
```
to watch each step run and complete.

When this workflow is done running, you will need to Control+C to get your terminal back.

In this example we submitted quite a few "no-op" jobs, but
the behavior is similar to what we saw in demo 1. `qlaunch rapidfire`
will keep launching jobs associated with both `onenode` and `twonode` tasks
until the database detects that they have completed. 

Take a look inside your `block_<date>` folder to see all of the jobs
FireWorks launched to complete this workflow. Check to see if you find
the same outputs as demo 1.

```
(fireworks)stephey@perlmutter:login36:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-10-04-45-27-649185> grep -r "attribute" .
./launcher_2023-04-10-04-46-37-996867/FW_job-7212373.out:pearson correlation coefficients for each attribute
(fireworks)stephey@perlmutter:login36:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-10-04-45-27-649185> cat ./launcher_2023-04-10-04-46-37-996867/FW_job-7212373.out
2023-04-09 21:46:41,758 INFO Hostname/IP lookup (this will take a few seconds)
2023-04-09 21:46:41,769 INFO Launching Rocket
2023-04-09 21:46:41,907 INFO RUNNING fw_id: 3 in directory: /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
2023-04-09 21:46:41,915 INFO Task started: ScriptTask.
pearson correlation coefficients for each attribute
                                   0
age                         0.187889
sex                         0.043062
body_mass_index             0.586450
blood_pressure              0.441482
total_cholesterol           0.212022
ldl_cholesterol             0.174054
hdl_cholesterol            -0.394789
total/hdl_cholesterol       0.430453
log_of_serum_triglycerides  0.565883
blood_sugar_level           0.382483
2023-04-09 21:46:42,564 INFO Task completed: ScriptTask
2023-04-09 21:46:42,579 INFO Rocket finished
(fireworks)stephey@perlmutter:login36:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC/block_2023-04-10-04-45-27-649185> 
```

Indeed we do!
