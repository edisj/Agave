import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
# Enable inline plotting  
%matplotlib inline

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

cores_per_node = {
                  '1': [1, 4, 8, 16, 28],
                  '2': [28, 42, 56],
                  '4': [84, 98, 112],
                  '6': [140, 154, 168],
                  '8': [196, 210, 224],
                  '12': [308, 322, 336],
                  '16': [420, 434, 448]
                  }

repeats = 3

def reduce_to_means(N, n):
    """Helper function to reduce data from numpy arrays.
    
    First it takes the mean across all ranks for each timing,
    then it takes the mean and standard deviation across the repeats.
    
    Parameters
    ----------
    n : int
        number of processes used in run
        
    Returns
    -------
    means : list
        mean across number of repeats for each timing
    stds : list
        standard deviation across repeats for each timing
        
    """
    
    init_total = np.empty(3)
    open_h5py = np.empty_like(init_total)
    io = np.empty_like(init_total)
    io_per_frame = np.empty_like(init_total)
    rmsd = np.empty_like(init_total)
    rmsd_per_frame = np.empty_like(init_total)
    comm_gather = np.empty_like(init_total)
    total = np.empty_like(init_total)

    _dict = {f'a{i}': np.load(f'{N}node_{i}/{n}process_times.npy') for i in range(1, repeats+1)}

    for i, array in enumerate(_dict.values()):
        init_total[i] = np.mean(array[:, 1])
        open_h5py[i] = np.mean(array[:, 2])
        io[i] = np.mean(array[:, 3])
        io_per_frame[i] = np.mean(array[:, 4])
        rmsd[i] = np.mean(array[:, 5])
        rmsd_per_frame[i] = np.mean(array[:, 6])
        comm_gather[i] = np.mean(array[:, 7])
        total[i] = np.mean(array[:, 8])

    means = [n, np.mean(init_total), np.mean(open_h5py), np.mean(io), np.mean(io_per_frame),
             np.mean(rmsd), np.mean(rmsd_per_frame), np.mean(comm_gather), np.mean(total)]
    stds = [n, np.std(init_total), np.std(open_h5py), np.std(io), np.std(io_per_frame),
             np.std(rmsd), np.std(rmsd_per_frame), np.std(comm_gather), np.std(total)]

    return means, stds
    
def all_process_dataframe():
    """Gives DataFrame of averaged timings for all N_process runs.
    
    Returns
    -------
    times_dframe : pd.DataFrame
        benchmark times with timings first averaged across all ranks, then averaged across repeats
    stds_dframe : pd.DataFrame 
        standard deviation of the timings when averaged across repeats   
    
    """
    columns = ['N_Processes', 'Total_Initialize', 'Initialize_h5py', 
               'IO', 'IO/Frame', 'RMSD', 'RMSD/Frame', 'Comm_Gather', 
               'Total_Benchmark_Time']
    
    data_buffer = np.empty(shape=(14,9), dtype=float)
    stds_buffer = np.empty(shape=(14,9), dtype=float)
    
    count = -1
    for N in [1,2,4,6]:
        for i, cores in enumerate(cores_per_node[f'{N}'], count+1):
            count = i
            means, stds = reduce_to_means(N, cores)
            for j in range(9):
                data_buffer[i, j] = means[j]
                stds_buffer[i, j] = stds[j]

    times_dframe = pd.DataFrame(list(data_buffer), columns=columns).set_index('N_Processes')
    stds_dframe = pd.DataFrame(list(stds_buffer), columns=columns).set_index('N_Processes')
            
    return times_dframe, stds_dframe
    
times, stds = all_process_dataframe()
