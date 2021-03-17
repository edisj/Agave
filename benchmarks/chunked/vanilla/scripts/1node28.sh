#!/bin/bash

#SBATCH -N 1  # number of nodes
#SBATCH -n 28  # number of cores
#SBATCH -t 0-2:00:00   # time in d-hh:mm:ss
#SBATCH -p parallel       # partition
#SBATCH -q normal       # QOS
#SBATCH -o 1node28.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e 1node28.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=ejakupov@asu.edu # Mail-to address

#echo commands to stdout
set -x

module purge
module load anaconda/py3
module load hdf5/1.10.1-gnu-stock-openmpi-3.0.0
source activate mda2

testdir=/scratch/ejakupov/Agave/temp/$SLURM_JOB_DEPENDENCY

export OMP_NUM_THREADS=1

mpiexec -n 28 python -W ignore /scratch/ejakupov/Agave/benchmarks/chunked/vanilla/scripts/benchmark.py $testdir/YiiP_system.pdb $testdir/YiiP_system_9ns_center100x_chunked.h5md $1/1node_$2

rm -r $testdir
