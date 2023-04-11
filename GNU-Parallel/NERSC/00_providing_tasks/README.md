
# Passing a List of Tasks to GNU Parallel

## Running the Example 

The example script can be run in this directory with the command:

    ./providing_tasks.sh

The expected output is available in the file expected_output.txt

### Pipe

Command line pipes can be used to send the tasks to GNU Parallel. This is most convenient for simple arrangments where a one-line command can work and writing any script isn't needed.

### File to Stdin

A file can be redirected to the stdin of GNU Parallel using a "<"

### Three Colon Notation
 
A GNU Parallel command with three colons (:::) accepts a list of tasks separated by spaces. 

### Four Colon Notation

A GNU Parallel command with four colons (::::) accepts a file path, and the content of that file is treated as a list of tasks.

## More Advanced Task Input

In general, the reason to choose colon inputs instead of the others is additional flexibility. Multiple three or four colon input lists can be passed to a single GNU Parallel command, and the result is the product of each list. This can remove the need for for loops somewhere else in the workflow where all combinations of items from two lists need to be iterated through. 

Additionally, a plus sign (+) can be appended to the colon notation to change the combination method to a dot product. Contrast these two examples:

> ::: 1 2 ::: a b
>
> outcome:
>
> 1 a
>
> 1 b
>
> 2 a
>
> 2 b

> :::+ 1 2 ::: a b
>
> outcome:
>
> 1 a
>
> 2 b

