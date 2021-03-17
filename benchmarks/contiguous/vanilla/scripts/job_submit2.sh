#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/2node28.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/2node42.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/4node84.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/4node98.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/6node140.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/6node154.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/8node196.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/8node210.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/12node308.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/contiguous/vanilla/scripts/16node420.sh $1 $repeat
done
