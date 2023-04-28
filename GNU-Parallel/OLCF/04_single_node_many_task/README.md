input.txt was created with this command: seq 1 12 > input.txt

[ketan2@login2.crusher 04_single_node_many_task]$ sbatch single_node_many_task_with_parallel.sh 

Submitted batch job 302092

[ketan2@login2.crusher 04_single_node_many_task]$ squeue -u ketan2

JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)

302092     batch  payload   ketan2 PD       0:00      1 (Priority)


[ketan2@login2.crusher 04_single_node_many_task]$ cat payload-302092.out 

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

