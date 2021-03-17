#!/bin/bash

#SBATCH -N 1  # number of nodes
#SBATCH -n 1  # number of cores
#SBATCH -t 0-3:00:00   # time in d-hh:mm:ss
#SBATCH -p serial       # partition
#SBATCH -q normal       # QOS
#SBATCH -o %j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e %j.err # file to save job's STDERR (%j = JobId)

#echo commands to stdout
set -x

sbatch --dependency=$SLURM_JOB_ID $1 $2 $3

TEST_TOP=/scratch/ejakupov/Agave/datafiles/YiiP_system.pdb
TEST_TRAJ=/scratch/ejakupov/Agave/datafiles/YiiP_system_9ns_center100x_chunked.h5md

testdir=/scratch/ejakupov/Agave/temp/$SLURM_JOB_ID
mkdir -p $testdir
time cp $TEST_TOP $testdir
time cp $TEST_TRAJ $testdir
