#!/bin/bash

#SBATCH -N 12  # number of nodes
#SBATCH -n 336  # number of cores
#SBATCH -t 0-02:00:00   # time in d-hh:mm:ss
#SBATCH -p parallel       # partition
#SBATCH -C Broadwell
#SBATCH -q normal       # QOS
#SBATCH -o slurm.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=ejakupov@asu.edu # Mail-to address

#echo commands to stdout
set -x

module purge
module load anaconda/py3
module load hdf5/1.10.1-gnu-stock-openmpi-3.0.0
source activate mda2

TEST_TOP=/scratch/ejakupov/Agave/datafiles/YiiP_system.pdb
TEST_TRAJ=/scratch/ejakupov/Agave/datafiles/YiiP_system_9ns_center100x.h5md

testdir=/scratch/ejakupov/Agave/temp/$SLURM_JOB_ID
mkdir -p $testdir
cp $TEST_TOP $testdir
cp $TEST_TRAJ $testdir

export OMP_NUM_THREADS=1

for i in 308 322 336
do
    mpiexec -n $i python -W ignore /scratch/ejakupov/Agave/benchmarks/1-full_IO/scripts/benchmark.py $testdir/YiiP_system.pdb $testdir/YiiP_system_9ns_center100x.h5md $1
done

SLURM_OUTPUT=/scratch/ejakupov/Agave/benchmarks/1-full_IO/results/$1/slurm_output/12node
mkdir -p $SLURM_OUTPUT
mv slurm.$SLURM_JOB_ID.out $SLURM_OUTPUT
mv slurm.$SLURM_JOB_ID.err $SLURM_OUTPUT

rm -r $testdir
