#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/in_memory_2/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/in_memory_2/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/2node28.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/4node84.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/6node140.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/8node196.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/12node308.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/in_memory_2/scripts/16node420.sh $1 $repeat
done
