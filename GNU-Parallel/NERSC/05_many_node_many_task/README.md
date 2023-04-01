input.txt was created with this command: seq 1 12 > input.txt

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
