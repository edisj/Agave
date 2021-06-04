#!/bin/bash

#SBATCH -N 6  # number of nodes
#SBATCH -n 168  # number of cores
#SBATCH -t 0-02:00:00   # time in d-hh:mm:ss
#SBATCH -p parallel       # partition
#SBATCH -q normal       # QOS
#SBATCH -o slurm/slurm.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm/slurm.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=ejakupov@asu.edu # Mail-to address

module purge
module load anaconda/py3
module load hdf5/1.10.1-gnu-stock-openmpi-3.0.0
cd /home/ejakupov/
source activate mda2

TEST_TOP=/scratch/ejakupov/parallel_h5md/datafiles/YiiP_system.pdb
TEST_TRAJ=/scratch/ejakupov/parallel_h5md/datafiles/YiiP_system_9ns_center100x.h5md

testdir=/scratch/ejakupov/parallel_h5md/benchmarking/$SLURM_JOB_ID
mkdir -p $testdir
cp $TEST_TOP $testdir
cp $TEST_TRAJ $testdir

export OMP_NUM_THREADS=1

for i in 140 154 168
do
    mpiexec -n $i python /scratch/ejakupov/parallel_h5md/scripts/gen2/Agave/rmsd/90Kframe/rmsd_parallel_bench_100x.py $testdir/YiiP_system.pdb $testdir/YiiP_system_9ns_center100x.h5md $1
done

rm -r $testdir
