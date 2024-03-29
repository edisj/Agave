import MDAnalysis as mda
from MDAnalysis.analysis.rms import rmsd
from mpi4py import MPI
import numpy as np
import time
import datetime
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("test_top", help="Path to topology testfile")
parser.add_argument("test_traj", help="Path to trajectory testfile")
parser.add_argument("directory_name", help="Name of directory the benchmark"
                    "results will be stored in")
args = parser.parse_args()


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def benchmark(topology, trajectory):
    """Benchmarks rmsd calculation for a given universe"""
    with timeit() as init:
        with timeit() as init_top:
            u = mda.Universe(topology)
        with timeit() as init_traj:
            u.load_new(trajectory, driver="mpio", comm=MPI.COMM_WORLD)

        CA = u.select_atoms("protein and name CA")
        x_ref = CA.positions.copy()
        n_frames = len(u.trajectory)

        slices = make_balanced_slices(n_frames, size,
                                      start=0, stop=n_frames, step=1)
        # give each rank unique start and stop points
        start = slices[rank].start
        stop = slices[rank].stop
        bsize = stop - start
        # sendcounts is used for Gatherv() to know how many elements are sent
        # from each rank
        sendcounts = np.array([slices[i].stop - slices[i].start for i in range(size)])

    t_init = init.elapsed
    t_init_top = init_top.elapsed
    t_init_traj = init_traj.elapsed

    total_io = 0
    total_rmsd = 0
    rmsd_array = np.empty(bsize, dtype=float)
    total_copy_data = 0
    total_copy_box = 0
    total_get_dataset = 0
    total_set_ts_position = 0
    total_convert_units = 0
    for j, i in enumerate(range(start, stop)):
        # input/output time
        with timeit() as io:
            ts = u.trajectory[i]
        total_io += io.elapsed
        total_copy_data += ts.timing.copy_data
        total_copy_box += ts.timing.box
        total_get_dataset += ts.timing.get_position
        total_set_ts_position += ts.timing.set_position
        total_convert_units += ts.timing.convert_units
        # rmsd calculation time
        with timeit() as rms:
            rmsd_array[j] = rmsd(CA.positions, x_ref, superposition=True)
        total_rmsd += rms.elapsed
    t_open_traj = ts.timing.open_traj
    t_n_atoms = ts.timing.n_atoms
    t_set_units = ts.timing.set_units

    block_times = np.array((rank, t_init, t_init_top, t_init_traj, t_open_traj,
                            t_n_atoms, t_set_units,
                            total_io, total_io/bsize, total_copy_data, total_copy_box,
                            total_get_dataset, total_set_ts_position, total_convert_units,
                            total_rmsd, total_rmsd/bsize, 0., 0., 0.),
                            dtype=float)

    with timeit() as wait_time:
        comm.Barrier()
    t_wait = wait_time.elapsed

    # time how long it takes for proceses to gather the data
    with timeit() as comm_gather:
        rmsd_buffer = None
        if rank == 0:
            rmsd_buffer = np.empty(n_frames, dtype=float)
        comm.Gatherv(sendbuf=rmsd_array, recvbuf=(rmsd_buffer, sendcounts), root=0)
    t_comm_gather = comm_gather.elapsed

    # total benchmark time per rank
    total_time = t_init + total_io + total_rmsd + t_wait + t_comm_gather

    # gather communication and total times into rank 0
    t_wait = comm.gather(t_wait, root=0)
    t_comm_gather = comm.gather(t_comm_gather, root=0)
    total_time = comm.gather(total_time, root=0)

    # gather times from each block into times_array
    times_buffer = None
    if rank == 0:
        times_buffer = np.empty(19*size, dtype=float)
    comm.Gather(sendbuf=block_times, recvbuf=times_buffer, root=0)

    if rank == 0:
        # turn 1 dimensional vector into size x 20 matrix where the
        # columns are t_loop, t_rmsd, etc and rows are each rank
        times_buffer = times_buffer.reshape(size, 19)

        times_buffer[:, -3] = t_wait
        times_buffer[:, -2] = t_comm_gather
        times_buffer[:, -1] = total_time

        return times_buffer, rmsd_buffer

    return None, None


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


def make_balanced_slices(n_frames, n_blocks, start=None, stop=None, step=None):
    """Divide `n_frames` into `n_blocks` balanced blocks.
    The blocks are generated in such a way that they contain equal numbers of
    frames when possible, but there are also no empty blocks.
    Arguments
    ---------
    n_frames : int
        number of frames in the trajectory (≥0). This must be the
        number of frames *after* the trajectory has been sliced,
        i.e. ``len(u.trajectory[start:stop:step])``. If any of
        `start`, `stop, and `step` are not the defaults (left empty or
        set to ``None``) they must be provided as parameters.
    n_blocks : int
        number of blocks (>0 and <n_frames)
    start : int or None
        The first index of the trajectory (default is ``None``, which
        is interpreted as "first frame", i.e., 0).
    stop : int or None
        The index of the last frame + 1 (default is ``None``, which is
        interpreted as "up to and including the last frame".
    step : int or None
        Step size by which the trajectory is sliced; the default is
        ``None`` which corresponds to ``step=1``.
    Returns
    -------
    slices : list of slice
        List of length ``n_blocks`` with one :class:`slice`
        for each block.
        If `n_frames` = 0 then an empty list ``[]`` is returned.
    """

    start = int(start) if start is not None else 0
    stop = int(stop) if stop is not None else None
    step = int(step) if step is not None else 1

    if n_frames < 0:
        raise ValueError("n_frames must be >= 0")
    elif n_blocks < 1:
        raise ValueError("n_blocks must be > 0")
    elif n_frames != 0 and n_blocks > n_frames:
        raise ValueError(f"n_blocks must be smaller than n_frames: "
                         f"{n_frames}")
    elif start < 0:
        raise ValueError("start must be >= 0 or None")
    elif stop is not None and stop < start:
        raise ValueError("stop must be >= start and >= 0 or None")
    elif step < 1:
        raise ValueError("step must be > 0 or None")

    if n_frames == 0:
        # not very useful but allows calling code to work more gracefully
        return []

    bsizes = np.ones(n_blocks, dtype=np.int64) * n_frames // n_blocks
    bsizes += (np.arange(n_blocks, dtype=np.int64) < n_frames % n_blocks)
    # This can give a last index that is larger than the real last index;
    # this is not a problem for slicing but it's not pretty.
    # Example: original [0:20:3] -> n_frames=7, start=0, step=3:
    #          last frame 21 instead of 20
    bsizes *= step
    idx = np.cumsum(np.concatenate(([start], bsizes)))
    slices = [slice(bstart, bstop, step)
              for bstart, bstop in zip(idx[:-1], idx[1:])]

    # fix very last stop index: make sure it's within trajectory range or None
    # (no really critical because the slices will work regardless, but neater)
    last = slices[-1]
    last_stop = min(last.stop, stop) if stop is not None else stop
    slices[-1] = slice(last.start, last_stop, last.step)

    return slices


if __name__ == "__main__":

    topology, trajectory = (args.test_top, args.test_traj)

    times_array, rmsd_array = benchmark(topology, trajectory)

    if rank == 0:
        data_path = '/scratch/ejakupov/parallel_h5md/data/gen2/Agave/rmsd/90Kframe/'
        #date = str(datetime.date.today()) + '/'

        os.makedirs(os.path.join(data_path, args.directory_name + '/'), exist_ok=True)

        np.save(os.path.join(data_path, args.directory_name + '/',  f'{size}process_times.npy'), times_array)
        np.save(os.path.join(data_path, args.directory_name + '/',  f'{size}process_rmsd.npy'), rmsd_array)
