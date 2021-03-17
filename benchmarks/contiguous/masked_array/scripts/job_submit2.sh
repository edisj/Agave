#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/1node14.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/2node42.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/4node98.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/6node154.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/8node196.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/12node308.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/masked_array/scripts/16node420.sh $1 $repeat
done
