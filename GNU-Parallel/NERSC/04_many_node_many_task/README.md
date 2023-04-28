
# Example Running GNU Parallel in a Slurm Job with Multiple Nodes

This example uses a given input.txt file containing tasks, and executes them inside a Slurm job with multiple nodes on Perlmutter.

input.txt was created with this command:

    seq 1 12 > input.txt

Run the example for yourself with this command:

    sbatch many_node_many_task.sh input.txt -A ntrain7

If you've set the SBATCH_ACCOUNT environment variable, then the -A argument is not needed.

## Modifying for Yourself

Replace the example script with your own application by modifying driver.sh. Change the parallel command at the bottom to remove payload.sh and insert your task application and its arguments. After doing this, payload.sh is no longer needed. Remember that there will be one GNU Parallel running for each node in the job, so if you choose to use the --jobs flag, consider that this is limiting the number of tasks that can run in parallel on one node.

Choosing the number of nodes in your job can be done in two ways. 

Modify this line in many_node_many_task.sh to change the number of nodes your job will request:

    #SBATCH --nodes=2

Alternatively, your sbatch command could be given a --nodes=X flag.

    sbatch --nodes=3 many_node_many_task.sh input.txt -A ntrain7

## Demonstration

    warndt@perlmutter:login13:\~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/many_node_many_task> sbatch -A nstaff many_node_many_task.sh input.txt 
    Submitted batch job 6267031
    warndt@perlmutter:login13:\~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/many_node_many_task> sqs
    JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON
    6267031          PD warndt    many_node_ma  2          10:00       0:00  2023-03-20T16:14:27  debug           N/A                  cpu            (Priority)     
    warndt@perlmutter:login13:\~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/many_node_many_task> sqs
    JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON
    warndt@perlmutter:login13:\~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/many_node_many_task> cat slurm-6267031.out 
    This is the payload script. argument_2 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_4 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_8 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_10 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_12 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_6 is the argument passed to it. Ran on machine nid005639.
    This is the payload script. argument_1 is the argument passed to it. Ran on machine nid005640.
    This is the payload script. argument_5 is the argument passed to it. Ran on machine nid005640.
    This is the payload script. argument_3 is the argument passed to it. Ran on machine nid005640.
    This is the payload script. argument_7 is the argument passed to it. Ran on machine nid005640.
    This is the payload script. argument_9 is the argument passed to it. Ran on machine nid005640.
    This is the payload script. argument_11 is the argument passed to it. Ran on machine nid005640.
    warndt@perlmutter:login13:\~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/many_node_many_task> 
