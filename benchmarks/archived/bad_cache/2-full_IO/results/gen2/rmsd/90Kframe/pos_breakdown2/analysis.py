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
    init_top = np.empty_like(init_total)
    init_traj = np.empty_like(init_total)
    open_traj = np.empty_like(init_total)
    n_atoms = np.empty_like(init_total)
    set_units = np.empty_like(init_total)
    io = np.empty_like(init_total)
    io_per_frame = np.empty_like(init_total)
    copy_data = np.empty_like(init_total)
    copy_box = np.empty_like(init_total)
    get_dataset = np.empty_like(init_total)
    set_ts_position = np.empty_like(init_total)
    convert_units = np.empty_like(init_total)
    rmsd = np.empty_like(init_total)
    rmsd_per_frame = np.empty_like(init_total)
    wait = np.empty_like(init_total)
    comm_gather = np.empty_like(init_total)
    total = np.empty_like(init_total)

    _dict = {f'a{i}': np.load(f'{N}node_{i}/{n}process_times.npy') for i in range(1, repeats+1)}

    for i, array in enumerate(_dict.values()):
        init_total[i] = np.mean(array[:, 1])
        init_top[i] = np.mean(array[:, 2])
        init_traj[i] = np.mean(array[:, 3])
        open_traj[i] = np.mean(array[:, 4])
        n_atoms[i] = np.mean(array[:, 5])
        set_units[i] = np.mean(array[:, 6])
        io[i] = np.mean(array[:, 7])
        io_per_frame[i] = np.mean(array[:, 8])
        copy_data[i] = np.mean(array[:, 9])
        copy_box[i] = np.mean(array[:, 10])
        get_dataset[i] = np.mean(array[:, 11])
        set_ts_position[i] = np.mean(array[:, 12])
        convert_units[i] = np.mean(array[:, 13])
        rmsd[i] = np.mean(array[:, 14])
        rmsd_per_frame[i] = np.mean(array[:, 15])
        wait[i] = np.mean(array[:, 16])
        comm_gather[i] = np.mean(array[:, 17])
        total[i] = np.mean(array[:, 18])

    means = [n, np.mean(init_total), np.mean(init_top), np.mean(init_traj), np.mean(open_traj), 
             np.mean(n_atoms), np.mean(set_units), np.mean(io), np.mean(io_per_frame),
             np.mean(copy_data), np.mean(copy_box), np.mean(get_dataset), np.mean(set_ts_position), np.mean(convert_units),
             np.mean(rmsd), np.mean(rmsd_per_frame), np.mean(wait), np.mean(comm_gather), np.mean(total)]
    stds = [n, np.std(init_total), np.std(init_top), np.std(init_traj), np.std(open_traj), 
             np.std(n_atoms), np.std(set_units), np.std(io), np.std(io_per_frame),
             np.std(copy_data), np.std(copy_box), np.std(get_dataset), np.std(set_ts_position), np.std(convert_units),
             np.std(rmsd), np.std(rmsd_per_frame), np.std(wait), np.std(comm_gather), np.std(total)]

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
    columns = ['N_Processes', 'Total_Initialize', 'Initialize_Topology', 
                'Initialize_Trajectory', 'Open_Trajectory', 'Set_n_atoms',
                'Set_Units', 'IO', 'IO/Frame', 'Copy_Data', 'Copy_Box',
                'Get_Dataset', 'Set_ts_Position', 'Convert_Units',
                'RMSD', 'RMSD/Frame', 'Wait', 'Comm_Gather', 'Total_Benchmark_Time']
    
    data_buffer = np.empty(shape=(14,19), dtype=float)
    stds_buffer = np.empty(shape=(14,19), dtype=float)
    
    count = -1
    for N in [1,2,4,6]:
        for i, cores in enumerate(cores_per_node[f'{N}'], count+1):
            count = i
            means, stds = reduce_to_means(N, cores)
            for j in range(19):
                data_buffer[i, j] = means[j]
                stds_buffer[i, j] = stds[j]

    times_dframe = pd.DataFrame(list(data_buffer), columns=columns).set_index('N_Processes')
    stds_dframe = pd.DataFrame(list(stds_buffer), columns=columns).set_index('N_Processes')
            
    return times_dframe, stds_dframe
    
times, stds = all_process_dataframe()
