input.txt was created with this command: seq 1 12 > input.txt

elvis@perlmutter:login13:~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sbatch single_node_many_task_with_parallel.sh -A nstaff
Submitted batch job 6252243
elvis@perlmutter:login13:~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sqs
JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON
6252243          PD warndt    single_node_  1           2:00       0:00  2023-03-20T12:16:42  debug           N/A                  cpu            (Priority)     
elvis@perlmutter:login13:~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> sqs
JOBID            ST USER      NAME          NODES TIME_LIMIT       TIME  SUBMIT_TIME          QOS             START_TIME           FEATURES       NODELIST(REASON
elvis@perlmutter:login13:~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> cat slurm-6252243.out 
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
elvis@perlmutter:login13:~/DOE-HPC-workflow-training/GNU-Parallel/NERSC/single_node_many_task> 
