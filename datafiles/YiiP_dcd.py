import MDAnalysis as mda

top = '/scratch/ejakupov/Agave/datafiles/YiiP_system.pdb'
traj = '/scratch/ejakupov/Agave/datafiles/YiiP_system_9ns_center100x_contiguous.h5md'

u = mda.Universe(top, traj)

with mda.Writer("YiiP_system_9ns_center100x.dcd",
                n_atoms=u.trajectory.n_atoms,
                positions=True) as W:
    for ts in u.trajectory:
        W.write(u)
