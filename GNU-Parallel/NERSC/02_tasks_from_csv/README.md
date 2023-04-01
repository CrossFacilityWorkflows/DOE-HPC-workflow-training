This example is a demonstration of using the column separator flag to extract
different parts of each task input line.

The argument given to the --colsep flag specifies the boundary between tokens
of the input line. This example is a .csv file so we have given colsep the ","
character.

After choosing the columnn separator, each token can be referred to in the command by
placing an integer inside the substitution brackets. {1} will be replaced with
the first token, {2} will be replaced with the second token, and so on.

Note that GNU-parallel documentation mentions a --csv flag, but it does not work on Perlmutter.
This is because it uses a parser from the Text::CSV module, which is not installed in the system
perl on Perlmutter. If you really wanted to use that flag you could install your own copy of Perl,
obtain the Text::CSV module from CPAN, and modify your path such that parallel finds your Perl copy
before the system copy; relative to all that effort, it's much  easier to use --colsep with a
comma character.

elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/tasks_from_csv> cat input.csv 
"Bob","18","Cherry"
"Alice","9","Apple"
"Bort","1","Pipevine"
elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/tasks_from_csv> cat csv_parse.sh 
#!/bin/bash

module load parallel

parallel --colsep="," echo {1} {3} :::: $1
elvis@perlmutter:login13:~/work_work/DOE-HPC-workflow-training/GNU-Parallel/NERSC/tasks_from_csv> ./csv_parse.sh input.csv 
"Bob" "Cherry"
"Alice" "Apple"
"Bort" "Pipevine"
