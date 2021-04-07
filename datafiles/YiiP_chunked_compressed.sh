#!/bin/bash

#SBATCH -N 1  # number of nodes
#SBATCH -n 1  # number of cores
#SBATCH -t 0-3:00:00   # time in d-hh:mm:ss
#SBATCH -p serial       # partition
#SBATCH -q normal       # QOS
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=ejakupov@asu.edu # Mail-to address

module purge
module load anaconda/py3
module load hdf5/1.10.1-gnu-stock-openmpi-3.0.0
source activate mda2

python YiiP_chunked_compressed.py
