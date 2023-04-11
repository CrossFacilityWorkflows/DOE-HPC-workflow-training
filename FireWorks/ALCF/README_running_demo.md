# FireWorks demo at ALCF

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
natually suited to this kind of workflow and requires less configuration
so we'll start here. 

Let's start by looking at our high-throughput FireWork:

```
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat fw_diabetes_ht.yaml 

fws:
- fw_id: 1
  spec:
    _category: twonode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 1 python step_1_diabetes_preprocessing.py
- fw_id: 2
  spec:
    _category: twonode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 10 python step_2_diabetes_correlation.py
- fw_id: 3
  spec:
    _category: twonode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 1 python step_3_diabetes_postprocessing.py
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
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_fworker2.yaml 
name: two node fireworker
category: twonode
query: '{}'
```

Next, let's look at our `my_qadapter.yaml`. On ALCF Polaris we use a PBS adapter- on other systems, you can
substitue the [appropriate adapter](https://github.com/materialsproject/fireworks/tree/bd2bb5078122fa27a7dda2084abb3af8cac05436/fw_tutorials/queue).

Note that Polaris-specific changes to the PBS adapter haven't been
[merged](https://github.com/materialsproject/fireworks/pull/498) upstream, so for now
you'll need to modify the PBS template in your conda installation.

This file is located at `$CONDA_PREFIX/lib/python3.9/site-packages/fireworks/user_objects/queue_adapters/PBS_template.txt`

The modification you need to make is to add the `filesystems` PBS queue option immediately below
`#PBS -l pmem=$${pmem}` like so

```
#PBS -l pmem=$${pmem}
#PBS -l filesystems=$${filesystems}
```

Save your changes and exit.

Now that your PBS template is ready, let's take a look at our `my_qadapter.yaml`. Note you'll need
to change the paths to reflect your own setup.

```
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_qadapter.yaml
_fw_name: CommonAdapter
_fw_q_type: PBS
rocket_launch: rlaunch -l /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_launchpad.yaml -w /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_fworker2.yaml singleshot
nnodes: 2
ppnode: 1
walltime: '00:05:00'
queue: debug-scaling
account: WALSforAll
filesystems: home:eagle
job_name: null
logdir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/
pre_rocket: module load conda; conda activate fireworks
post_rocket: null
```

Things to note:
- We unfortuatnely have to specify the full paths
  to `my_launchpad.yaml` and `my_fworker2.yaml`- bash shortcuts
  are not supported.
- We have specified `singleshot` here, since each task within the workflow only needs to run once.
- We have specified the usual Slurm job resources that each task will use.
- Since PBS does not inherit the environment which we used to launch the job,
  we'll need to load our custom conda environment before each job runs.  

Now that we've examined all the pieces, let's run our FireWorks workflow.

We will launch the workflow with `qlaunch rapidfire`. Remember that we have
specified `rlaunch singleshot` in our queue adapter- this will run each task once per job.
However we need to launch 3 jobs, one for each task. For this reason we use `qlaunch rapidfire`
to automatically launch our whole workflow. `rapidfile` will keep launching jobs until
there are no more pending FireWorks in the database.

Note
we are issuing these commands from a Polaris login node with our `fireworks` conda
environment activated.

Due to [queue restrictions](https://docs.alcf.anl.gov/polaris/running-jobs/)
on Polaris, we will use `qlaunch rapidfire -m 1` to launch one job at a time
since we are using the `debug-scaling` queue. Other queues may not need this
restriction. 

```
(2022-09-08/fireworks) stephey@polaris-login-02:~/DOE-HPC-workflow-training/FireWorks/ALCF> qlaunch rapidfire -m 1
2023-04-11 00:38:09,568 INFO getting queue adapter
2023-04-11 00:38:09,570 INFO Created new dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570
2023-04-11 00:38:09,655 INFO The number of jobs currently in the queue is: 0
2023-04-11 00:38:09,656 INFO 0 jobs in queue. Maximum allowed by user: 1
2023-04-11 00:38:09,688 INFO Launching a rocket!
2023-04-11 00:38:09,695 INFO Created new dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-38-09-694941
2023-04-11 00:38:09,695 INFO moving to launch_dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-38-09-694941
2023-04-11 00:38:09,698 INFO submitting queue script
2023-04-11 00:38:09,939 INFO Job submission was successful and job_id is 477639
2023-04-11 00:38:09,939 INFO Sleeping for 5 seconds...zzz...
2023-04-11 00:38:14,951 INFO Jobs in queue (1) meets/exceeds maximum allowed (1)
2023-04-11 00:38:14,956 INFO Finished a round of launches, sleeping for 60 secs
2023-04-11 00:39:15,016 INFO Checking for Rockets to run...
2023-04-11 00:39:15,072 INFO The number of jobs currently in the queue is: 0
2023-04-11 00:39:15,073 INFO 0 jobs in queue. Maximum allowed by user: 1
2023-04-11 00:39:15,080 INFO Launching a rocket!
2023-04-11 00:39:15,087 INFO Created new dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-39-15-086463
2023-04-11 00:39:15,087 INFO moving to launch_dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-39-15-086463
2023-04-11 00:39:15,090 INFO submitting queue script
2023-04-11 00:39:15,330 INFO Job submission was successful and job_id is 477640
2023-04-11 00:39:15,331 INFO Sleeping for 5 seconds...zzz...
2023-04-11 00:39:20,343 INFO Jobs in queue (1) meets/exceeds maximum allowed (1)
2023-04-11 00:39:20,348 INFO Finished a round of launches, sleeping for 60 secs
2023-04-11 00:40:20,408 INFO Checking for Rockets to run...
2023-04-11 00:40:20,464 INFO The number of jobs currently in the queue is: 0
2023-04-11 00:40:20,464 INFO 0 jobs in queue. Maximum allowed by user: 1
2023-04-11 00:40:20,473 INFO Launching a rocket!
2023-04-11 00:40:20,480 INFO Created new dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-40-20-479394
2023-04-11 00:40:20,480 INFO moving to launch_dir /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-00-38-09-569570/launcher_2023-04-11-00-40-20-479394
2023-04-11 00:40:20,483 INFO submitting queue script
2023-04-11 00:40:20,763 INFO Job submission was successful and job_id is 477641
2023-04-11 00:40:20,764 INFO Sleeping for 5 seconds...zzz...
2023-04-11 00:40:25,776 INFO Jobs in queue (1) meets/exceeds maximum allowed (1)
2023-04-11 00:40:25,780 INFO Finished a round of launches, sleeping for 60 secs
2023-04-11 00:41:25,840 INFO Checking for Rockets to run...
2023-04-11 00:41:25,895 INFO The number of jobs currently in the queue is: 0
2023-04-11 00:41:25,895 INFO 0 jobs in queue. Maximum allowed by user: 1
```

We can query the status of our workflow in another terminal. After a few minutes
you should see

```
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> lpad get_fws
[
    {
        "fw_id": 1,
        "created_on": "2023-04-11T00:37:59.961412",
        "updated_on": "2023-04-11T00:38:20.326142",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 2,
        "created_on": "2023-04-11T00:37:59.961634",
        "updated_on": "2023-04-11T00:39:25.305963",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 3,
        "created_on": "2023-04-11T00:37:59.961775",
        "updated_on": "2023-04-11T00:40:30.423533",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    }
]
```

FireWorks lists all of our tasks as successfully completed.

Let's take a look in our `block_<date>` directory to see what
FireWorks did. Note that in this directory, there may be more
`launcher_<date>` directories than steps in our workflow.
This is because FireWorks has no visibility into the current
state of the queue- it just launches jobs every minute
while the database reports there are pending workflow steps.

## Demo 2- heterogenous workflow

Let's make things a little more complicated now. In this version of the demo,
we'll have a workflow where step 1 and step 3 only use one node, but step 2
uses two nodes.

Let's start by looking at our `fw_diabetes_wf.yaml` file

```
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat fw_diabetes_wf.yaml 
fws:
- fw_id: 1
  spec:
    _category: onenode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF 
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 1 python step_1_diabetes_preprocessing.py
- fw_id: 2
  spec:
    _category: twonode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 10 python step_2_diabetes_correlation.py
- fw_id: 3
  spec:
    _category: onenode
    _launch_dir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
    _tasks:
    - _fw_name: ScriptTask
      script: mpiexec -n 1 python step_3_diabetes_postprocessing.py
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
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_fworker1.yaml 
name: one node fireworker
category: onenode
query: '{}'
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_fworker2.yaml 
name: two node fireworker
category: twonode
query: '{}
```

Note that this is the same `my_fworker2.yaml` that we used in demo 1.

Because we need to specify different sets of resources to our scheduler,
we also need to have two queue adapters- one for the `onenode` case and one
for the `twonode` case:

```
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_qadapter1.yaml 
_fw_name: CommonAdapter
_fw_q_type: PBS
rocket_launch: rlaunch -l /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_launchpad.yaml -w /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_fworker1.yaml singleshot
nnodes: 1
ppnode: 1
walltime: '00:05:00'
queue: preemptable
account: WALSforAll
filesystems: home:eagle
job_name: null
logdir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/
pre_rocket: module load conda; conda activate fireworks
post_rocket: null
(2022-09-08/fireworks) stephey@polaris-login-01:~/DOE-HPC-workflow-training/FireWorks/ALCF> cat my_qadapter2.yaml 
_fw_name: CommonAdapter
_fw_q_type: PBS
rocket_launch: rlaunch -l /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_launchpad.yaml -w /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/my_fworker2.yaml singleshot
nnodes: 2
ppnode: 1
walltime: '00:05:00'
queue: preemptable
account: WALSforAll
filesystems: home:eagle
job_name: null
logdir: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF/
pre_rocket: module load conda; conda activate fireworks
post_rocket: null
```

We are ready to launch our heterogeneous workflow example. 

Recall that in our first example we did a
simple `qlaunch rapidfire -m 1`. We did not specify a specific queue adapter here. If we do not
specify a specific queue adpater, FireWorks will chose the default file, `my_qadapter.yaml`.

However in this example, we will have to launch our workflow using both queue adapters
`my_qadapter1.yaml` and `my_qadapter2.yaml`. Note that we specify the corresponding
`my_fworker1.yaml` and `my_fworker2.yaml`, respectively, in each queue adpater
file.

To launch our workflow, we'll issue two simultaneous `qlaunch rapidfire` commands. Note
we are issuing these commands from a Polaris login node with our `fireworks` conda
environment activated.

To launch our workflow, we'll issue two simultaneous `qlaunch rapidfire` commands.

```
lpad reset
lpad add fw_diabetes_wf.yaml
qlaunch -q my_qadapter1.yaml rapidfire -m 1 & qlaunch -q my_qadapter2.yaml rapidfire -m 1
```

Note we are limiting the number of jobs we allow FireWorks to submit due to the
[Polaris queue policies](https://docs.alcf.anl.gov/polaris/running-jobs/).

If you like, you can open a second terimnal to monitor the job status with
```
lpad get_fws
```
to watch each step run and complete.

When this workflow is done running, you may need to Control+C to get your terminal back.

In this example we submitted quite a few "no-op" jobs, but
the behavior is similar to what we saw in demo 1. `qlaunch rapidfire`
will keep launching jobs associated with both `onenode` and `twonode` tasks
until the database detects that they have completed. 

Take a look inside your `block_<date>` folder to see all of the jobs
FireWorks launched to complete this workflow. Check to see if you find
the same outputs as demo 1.

```
(2022-09-08/fireworks) stephey@polaris-login-04:~/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-17-46-48-104096> grep -r "attribute" .
./launcher_2023-04-11-17-48-51-801326/FW_job.out:pearson correlation coefficients for each attribute
(2022-09-08/fireworks) stephey@polaris-login-04:~/DOE-HPC-workflow-training/FireWorks/ALCF/block_2023-04-11-17-46-48-104096> cat ./launcher_2023-04-11-17-48-51-801326/FW_job.out
2023-04-11 17:48:58,901 INFO Hostname/IP lookup (this will take a few seconds)
2023-04-11 17:48:58,903 INFO Launching Rocket
2023-04-11 17:48:58,966 INFO RUNNING fw_id: 3 in directory: /home/stephey/DOE-HPC-workflow-training/FireWorks/ALCF
2023-04-11 17:48:58,972 INFO Task started: ScriptTask.
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
2023-04-11 17:48:59,417 INFO Task completed: ScriptTask
2023-04-11 17:48:59,426 INFO Rocket finished
```

Indeed we do!
