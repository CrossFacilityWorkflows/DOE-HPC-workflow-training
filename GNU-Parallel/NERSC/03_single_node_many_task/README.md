
# Example Running GNU Parallel in a single node Perlmutter job

This example uses a given input.txt file containing tasks, and executes them inside a Slurm job on Perlmutter.

input.txt was created with this command: 

    seq 1 12 > input.txt

Run the example for yourself with this command:

    sbatch single_node_many_task_with_parallel.sh -A ntrain7

If you've set the SBATCH_ACCOUNT environment variable, then the -A argument is not needed.

## The --jobs Flag

This example includes a --jobs 6 flag. This instructs GNU parallel to not run more than 6 jobs at the same time; the 7th job will wait until the first has finished. Without this flag GNU Parallel will continue launching tasks until it reaches the number of cores available on the processer. Sometimes you may know you want to run a different number. 

Some possible reasons to use the --job flag are: 

- Your tasks use more memory than the memory per core available on the node. The --jobs flag can be used to prevent an out of memory error.
- Tasks are very I/O intensive. If a large number of tasks saturate the filesystem, performance can suffer. Reducing the number of concurrent jobs can lead to better throughput.

## Demonstration of usage

    elvis@perlmutter:login13:\~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sbatch single_node_many_task_with_parallel.sh -A nstaff
    Submitted batch job 6252243
    elvis@perlmutter:login13:\~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sqs
    JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES  NODELIST(REASON)
    6252243          PD warndt    single_node_  1           2:00       0:00  2023-03-20T12:16:42  debug           N/A                  cpu            (Priority)
    elvis@perlmutter:login13:\~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sqs
    JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON)
    elvis@perlmutter:login13:\~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> cat slurm-6252243.out 
    This is the payload script. argument_1 is the argument passed to it.
    This is the payload script. argument_2 is the argument passed to it.
    This is the payload script. argument_3 is the argument passed to it.
    This is the payload script. argument_4 is the argument passed to it.
    This is the payload script. argument_5 is the argument passed to it.
    This is the payload script. argument_6 is the argument passed to it.
    This is the payload script. argument_7 is the argument passed to it.
    This is the payload script. argument_8 is the argument passed to it.
    This is the payload script. argument_9 is the argument passed to it.
    This is the payload script. argument_10 is the argument passed to it.
    This is the payload script. argument_11 is the argument passed to it.
    This is the payload script. argument_12 is the argument passed to it.
    elvis@perlmutter:login13:\~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> 

## Changing the Example to Use for Yourself

The only modifications needed to change single_node_many_task_with_parallel.sh to run your own application is to replace payload.sh with your own script or executable and change the task input brackets to match the arguments your application expects.
