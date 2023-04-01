#!/bin/bash

find $PWD -type f | grep txt | sort > tasks

module load parallel

parallel "cat {} > {//}/{/.}.output" :::: tasks
