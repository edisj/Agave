#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/contiguous/writer/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/contiguous/writer/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/2node42.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/4node98.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/6node154.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/writer/scripts/8node210.sh $1 $repeat
done
