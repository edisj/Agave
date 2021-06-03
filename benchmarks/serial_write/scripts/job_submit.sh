#!/bin/bash

DIR_NAME=$1

mkdir -p /scratch/ejakupov/Agave/benchmarks/serial_write/results/$DIR_NAME/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/serial_write/results/$DIR_NAME/slurm_output

for repeat in 1 2 3 4 5
do
    sbatch /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/job_script.sh $DIR_NAME $repeat xtc
    sbatch /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/job_script.sh $DIR_NAME $repeat dcd
    sbatch /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/serial_write/scripts/job_script.sh $DIR_NAME $repeat trr
done
