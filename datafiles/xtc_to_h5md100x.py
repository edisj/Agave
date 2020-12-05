import MDAnalysis as mda
import pyh5md
from MDAnalysisData import datasets


def create_test_trj(uni, filename):
    """uses pyh5md library to write h5md file"""

    with pyh5md.File(filename, 'w', creator='xtc_to_h5md_small.py') as f:
        trajectory = f.particles_group('trajectory')
        obsv = f.require_group('observables')

        positions = pyh5md.element(trajectory, 'position', store='time',
                                   data=uni.trajectory.ts.positions,
                                   time=True)
        f['particles/trajectory/position/value'].attrs['unit'] = 'Angstrom'
        f['particles/trajectory/position/time'].attrs['unit'] = 'ps'

        data_step = pyh5md.element(obsv, 'step',
                                   data=uni.trajectory.ts.data['step'],
                                   step_from=positions,
                                   store='time', time=True)

        trajectory.create_box(dimension=3,
                              boundary=['periodic', 'periodic', 'periodic'],
                              store='time',
                              data=uni.trajectory.ts.triclinic_dimensions,
                              step_from=positions)
        f['particles/trajectory/box/edges/value'].attrs['unit'] = 'Angstrom'

        for ts in uni.trajectory:
            trajectory.box.edges.append(uni.trajectory.ts.triclinic_dimensions,
                                        ts.frame, time=ts.time)
            positions.append(uni.trajectory.ts.positions,
                             ts.frame, time=ts.time)
            data_step.append(uni.trajectory.ts.data['step'],
                             ts.frame, time=ts.time)



def main():
    yiip = datasets.fetch_yiip_equilibrium_short()

    u = mda.Universe(yiip.topology, 100*[yiip.trajectory])
    create_test_trj(u, '/scratch/ejakupov/parallel_h5md/datafiles/YiiP_system_9ns_center100x.h5md')


if __name__ == '__main__':
    main()
