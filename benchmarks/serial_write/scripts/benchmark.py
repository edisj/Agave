import MDAnalysis as mda
from MDAnalysis.analysis.rms import rmsd
import numpy as np
import pandas as pd
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("test_top", help="Path to topology testfile")
parser.add_argument("test_traj", help="Path to trajectory testfile")
parser.add_argument("directory_name", help="Name of directory the benchmark"
                    "results will be stored in")
args = parser.parse_args()
trial_number = args.directory_name[-1]

root, ext = os.path.splitext(args.test_traj)

def benchmark(topology, trajectory):
    """Benchmarks rmsd calculation for a given universe"""
    u = mda.Universe(topology, trajectory)
    n_frames = len(u.trajectory)

    t_read = 0
    t_write = 0
    with timeit() as write_time:
        with mda.Writer(f"/scratch/ejakupov/Agave/temp/writer_benchmark/{ext.strip('.')}_throw_away_{trial_number}.h5md",
                        n_atoms=n_atoms,
                        positions=True, velocities=False, forces=False) as W:
            for frame in range(n_frames):
                with timeit() as read_frame:
                    u.trajectory[frame]
                with timeit() as write_frame:
                    W.write(u)
                t_read += read_frame.elapsed
                t_write += write_frame.elapsed
    write_and_read = write_time.elapsed

    times = np.array((write_and_read, t_read, t_write), dtype=float)

    return times

if __name__ == "__main__":

    topology, trajectory = (args.test_top, args.test_traj)

    times_array = benchmark(topology, trajectory)

    if rank == 0:
        data_path = '/scratch/ejakupov/Agave/benchmarks/serial_write/results/'

        os.makedirs(os.path.join(data_path, args.directory_name + '/'), exist_ok=True)

        np.save(os.path.join(data_path, args.directory_name + '/',  f'{size}process_times.npy'), times_array)

        columns = ['Write and Read', 'Read Time', 'Write Time']
        df = pd.DataFrame(times_array, columns=columns)
        df.to_csv(os.path.join(data_path, args.directory_name + '/',  f'{size}processes.csv'))
