#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/3-full_node/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/3-full_node/results/$1/slurm_output

for repeat in 1 2 3
do
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/1node1.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/1node28.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/2node.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/4node.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/6node.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/8node.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/12node.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/copy_file.sh /scratch/ejakupov/Agave/benchmarks/3-full_node/scripts/16node.sh $1 $repeat
done
