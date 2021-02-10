#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/h5py/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/h5py/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/h5py/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/h5py/scripts/1node14.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/h5py/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/h5py/scripts/2node42.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/h5py/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/h5py/scripts/4node98.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/h5py/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/h5py/scripts/6node154.sh $1 $repeat
done
