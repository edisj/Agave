#!/bin/bash

mkdir -p /scratch/ejakupov/Agave/benchmarks/serial/results/$1/slurm_output
cd /scratch/ejakupov/Agave/benchmarks/serial/results/$1/slurm_output

for repeat in 1 2 3 4 5
do
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_h5md_default.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/h5md_default.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_h5md_chunked.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/h5md_chunked.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_h5md_contiguous.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/h5md_contiguous.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_xtc.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/xtc.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_dcd.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/dcd.sh $1 $repeat
    sbatch /scratch/ejakupov/Agave/benchmarks/serial/scripts/copy_trr.sh /scratch/ejakupov/Agave/benchmarks/serial/scripts/trr.sh $1 $repeat
done
