#!/bin/bash

module load parallel

seq 4 8 | parallel echo "seq pipe argument {}"

parallel echo "stdin redirect argument {}" < tasks.txt

parallel echo "three colon argument {}" ::: 4 5 6 7 8

parallel echo "four colon argument {}" :::: tasks.txt
