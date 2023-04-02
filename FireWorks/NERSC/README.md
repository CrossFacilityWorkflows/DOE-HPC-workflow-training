# FireWorks at NERSC

First step towards creating FireWorks demo/tutorial at NERSC.

Is supposed to be a 3 part workflow, where step 1 depends on step 2 
and step 2 depends on step 3. Additionally, step 2 will use more resources
than steps 1 or 3 to run an MPI-based processing task.

The goal is to mimic the structure of a real scientific workflow,
even though the size of the dataset here is relatively small.

## Dataset

We're using the open source [Diabetes dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset)
that comes pre-installed in the `scikit-learn` package.

## Installing the environment

Note that I could not get all the depencies to resolve with Python 3.10, so 
I'm using Python 3.9. 

```
module load python
conda create -n fireworks python=3.9 -y
conda activate fireworks
conda install -c conda-forge fireworks pytest numpy scikit-learn pandas
MPICC="cc -shared" pip install --force-reinstall --no-cache-dir --no-binary=mpi4py mpi4py
```

#To Run

```
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> lpad reset
Are you sure? This will RESET 1 workflows and all data. (Y/N)y
2023-04-02 16:39:29,066 INFO Performing db tune-up
2023-04-02 16:39:29,123 INFO LaunchPad was RESET.
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> lpad add fw_diabetes_wf.yaml 
2023-04-02 16:40:19,383 INFO Added a workflow. id_map: {1: 1, 2: 2, 3: 3}
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> qlaunch -q my_qadapter1.yaml -w my_fworker1.yaml singleshot
2023-04-02 16:40:29,920 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
2023-04-02 16:40:29,923 INFO submitting queue script
2023-04-02 16:40:30,501 INFO Job submission was successful and job_id is 6888339
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> qlaunch -q my_qadapter2.yaml -w my_fworker2.yaml singleshot
2023-04-02 16:40:41,874 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
2023-04-02 16:40:41,877 INFO submitting queue script
2023-04-02 16:40:42,002 INFO Job submission was successful and job_id is 6888340
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> sqs
JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON
6888340          PD stephey   FW_job        2           5:00       0:00  2023-04-02T16:40:41  debug           N/A                  cpu            (Priority)     
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> lpad get_fws
[
    {
        "fw_id": 1,
        "created_on": "2023-04-02T23:40:19.376736",
        "updated_on": "2023-04-02T23:40:34.432363",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 2,
        "created_on": "2023-04-02T23:40:19.376920",
        "updated_on": "2023-04-02T23:40:55.705376",
        "state": "COMPLETED",
        "name": "Unnamed FW"
    },
    {
        "fw_id": 3,
        "created_on": "2023-04-02T23:40:19.377040",
        "updated_on": "2023-04-02T23:40:55.706743",
        "state": "READY",
        "name": "Unnamed FW"
    }
]
(/global/common/software/das/stephey/conda/conda_envs/fireworks) stephey@perlmutter:login35:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> qlaunch -q my_qadapter1.yaml -w my_fworker1.yaml singleshot
2023-04-02 16:41:08,583 INFO moving to launch_dir /pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC
2023-04-02 16:41:08,589 INFO submitting queue script
2023-04-02 16:41:08,713 INFO Job submission was successful and job_id is 6888341
```

