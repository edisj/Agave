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

def benchmark(topology, trajectory):
    """Benchmarks rmsd calculation for a given universe"""
    with timeit() as init:
        with timeit() as init_top:
            u = mda.Universe(topology)
        with timeit() as init_traj:
            u.load_new(trajectory)

        CA = u.select_atoms("protein and name CA")
        x_ref = CA.positions.copy()
        n_frames = len(u.trajectory)

    t_init = init.elapsed
    t_init_top = init_top.elapsed
    t_init_traj = init_traj.elapsed

    # intialize time counters
    total_io = 0
    total_rmsd = 0
    rmsd_array = np.empty(n_frames, dtype=float)
    for i, frame in enumerate(range(n_frames)):
        # input/output time
        with timeit() as io:
            ts = u.trajectory[frame]
        total_io += io.elapsed
        # rmsd calculation time
        with timeit() as rms:
            rmsd_array[i] = rmsd(CA.positions, x_ref, superposition=True)
        total_rmsd += rms.elapsed

    with timeit() as close_traj:
        u.trajectory.close()
    t_close_traj = close_traj.elapsed

    # total benchmark time
    total_time = t_init + total_io + total_rmsd + t_close_traj

    # collect all timings into this array
    block_times = np.array((t_init, t_init_top, t_init_traj,
                            total_io, total_io/n_frames,
                            total_rmsd, total_rmsd/n_frames,
                            t_close_traj, total_time),
                            dtype=float)

    return block_times, rmsd_array


class timeit(object):
    """measure time spend in context
    :class:`timeit` is a context manager (to be used with the :keyword:`with`
    statement) that records the execution time for the enclosed context block
    in :attr:`elapsed`.
    Attributes
    ----------
    elapsed : float
        Time in seconds that elapsed between entering
        and exiting the context.
    """
    def __enter__(self):
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        self.elapsed = end_time - self._start_time
        # always propagate exceptions forward
        return False


if __name__ == "__main__":

    topology, trajectory = (args.test_top, args.test_traj)

    times_array, rmsd_array = benchmark(topology, trajectory)

    data_path = '/scratch/ejakupov/Agave/benchmarks/serial/results/'
    filename = args.test_traj.split(sep='/')[-1].split(sep='.')[0]

    os.makedirs(os.path.join(data_path, args.directory_name + '/'), exist_ok=True)

    np.save(os.path.join(data_path, args.directory_name + '/',  f'{filename}_times.npy'), times_array)
    np.save(os.path.join(data_path, args.directory_name + '/',  f'{filename}_rmsd.npy'), rmsd_array)

    columns = ['t_init', 't_init_top', 't_init_traj',
                't_io', 't_io/frame',
                't_rmsd', 't_rmsd/frame',
                't_close_traj', 'total_time']
    df = pd.DataFrame(times_array.reshape(-1,len(times_array)), columns=columns)
    df.to_csv(os.path.join(data_path, args.directory_name + '/',  f'{filename}.csv'))
