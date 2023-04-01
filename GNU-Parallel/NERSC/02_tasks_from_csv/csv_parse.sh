#!/bin/bash

module load parallel

parallel --colsep="," echo {1} {3} :::: $1
