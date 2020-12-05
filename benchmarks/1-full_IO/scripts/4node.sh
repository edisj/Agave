#!/bin/bash

#SBATCH -N 4  # number of nodes
#SBATCH -n 112  # number of cores
#SBATCH -t 0-02:00:00   # time in d-hh:mm:ss
#SBATCH -p parallel       # partition
#SBATCH -C Broadwell
#SBATCH -q normal       # QOS
#SBATCH -o slurm/slurm.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm/slurm.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=ejakupov@asu.edu # Mail-to address

#echo commands to stdout
set -x

cd /home/ejakupov/
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

for i in 84 98 112
do
    mpiexec -n $i python /scratch/ejakupov/Agave/benchmarks/1-full_IO/benchmark.py $testdir/YiiP_system.pdb $testdir/YiiP_system_9ns_center100x.h5md $1
done

mkdir -p /scratch/ejakupov/Agave/benchmarks/results/$1/slurm_output/1node
cp slurm/slurm.$SLURM_JOB_ID.out /scratch/ejakupov/Agave/benchmarks/results/$1/slurm_output/1node
cp slurm/slurm.$SLURM_JOB_ID.err /scratch/ejakupov/Agave/benchmarks/results/$1/slurm_output/1node

rm -r $testdir
