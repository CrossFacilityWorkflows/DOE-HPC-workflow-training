# Using the Find Command to Make Task Input Files

This example demonstrates the use of the find command to build
a GNU parallel task list for a pre-existing data directory.

The data directory starts out with these contents:

    elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input/data> ls -lh
    total 1.5K
    -rw-rw---- 1 warndt warndt 25 Mar 31 16:36 task_1.txt
    -rw-rw---- 1 warndt warndt 25 Mar 31 16:36 task_two.txt
    -rw-rw---- 1 warndt warndt 29 Mar 31 16:36 tsk-3.txt
    elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input/data> cat *
    Input for task number 1.
    Input for task number 2.
    Input for task number three.

The goal is to process each of these files with a parallel command, and to keep the output files organized by naming them
based on the input filename while also writing them to the same location as the input.

This begins with the find command found in build_then_use_task_list.sh:
    find $PWD -type f | grep txt | sort > tasks
 
The find command will recursively report descendent files from the path it is given, in this case the content of the $PWD variable reports our working directory:
    elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input> echo $PWD
    /global/homes/e/elvis/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input

This is piped to a grep command which seeks only file paths containing "txt" (the extension present on example data files).
Careful the search string doesn't include any substrings from the path in $PWD.

The remaining data files and their full path is sorted and placed in the "tasks" file.

Next, the script loads the parallel module, and runs this parallel command:
    parallel "cat {} > {//}/{/.}.output" :::: tasks

Note the command is in quotes; this is needed when the redirect character (>) is present.
The cat command opens the filename and, through its full path, and prints the output to a constructed filename and path.
This introduces some variations of the GNU parallel substitution brackets: Inserting two slashes {//} modifies a path
by removing the filename and extension, leaving only the directory portion. Second, there is a {/.} substitution
which removes the directory path and the extension, leaving only the filename. 

Using these two substitutions, a "/" character, and an ".output" extension, we can create
a path and name for the output file which will appear in the same location as the input, have the same name as the input file but with a distinct ".output" extension. 
Thus, the same script can be reused on similar data directories anywhere
on the filesystem, and the outputs will be neatly organized relative to the inputs.

See the expected state of the data directory after running build_then_use_task_list.sh: 

    elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input/data> ls -lh
    total 3.0K
    -rw-rw---- 1 warndt warndt 25 Mar 31 21:27 task_1.output
    -rw-rw---- 1 warndt warndt 25 Mar 31 16:36 task_1.txt
    -rw-rw---- 1 warndt warndt 25 Mar 31 21:27 task_two.output
    -rw-rw---- 1 warndt warndt 25 Mar 31 16:36 task_two.txt
    -rw-rw---- 1 warndt warndt 29 Mar 31 21:27 tsk-3.output
    -rw-rw---- 1 warndt warndt 29 Mar 31 16:36 tsk-3.txt
    elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/01_using_find_to_make_input/data> cat *
    Input for task number 1.
    Input for task number 1.
    Input for task number 2.
    Input for task number 2.
    Input for task number three.
    Input for task number three.

