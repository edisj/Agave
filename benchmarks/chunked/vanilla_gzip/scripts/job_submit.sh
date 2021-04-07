#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/1node1.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/1node4.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/1node8.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/1node14.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/1node28.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/2node56.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/4node112.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/6node168.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/8node224.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/12node336.sh $1 $repeat
    #sbatch /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/chunked/vanilla_gzip/scripts/16node448.sh $1 $repeat
done
