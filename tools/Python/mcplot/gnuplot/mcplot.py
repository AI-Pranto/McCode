#!/usr/bin/env python
#
#  mcplot-gnuplot program. 
#
#  Use --noqt to omit loading of the qt gui interface (for non-qt, non-Perl systems).
#
import os
import argparse
import logging
from mcgnuplotter import McGnuplotter

def main(args):
    logging.basicConfig(level=logging.INFO)
    
    if args.simulation:
        simulation = args.simulation[0]
    else:
        simulation = 'mccode.sim'
    logging.debug('simulation file/dir: %s', simulation)
    
    if os.path.isdir(simulation):
        simulation = os.path.join(simulation, 'mccode.sim')
    
    if not os.path.isfile(simulation):
        print('Sim file not found')
        exit()
        
    if os.path.splitext(simulation)[1] == '.sim':
        print('Using sim file: %s' % os.path.abspath(simulation)) 
        plotter = McGnuplotter(simulation, noqt=args.noqt)
    else:
        dat_file = simulation
        print('Plot single monitor')
        plotter = McGnuplotter(dat_file, noqt=args.noqt)
    
    if args.noqt:
        keys = plotter.get_data_keys()
        plotter.plot(keys[0], args.logscale)
        exit()
    else:
        print('Loading qt gui...')
        exec('import mcgnuview')
        exec('mcgnuview.startGui(plotter, args.logscale)')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('simulation', nargs='*', help='simulation file (.sim), monitor file (.dat), directory, or none (current dir)')
    parser.add_argument('-n', '--noqt', action="store_true", default=False, help='plot simulation in gnuplot and exit')
    parser.add_argument('-l','--logscale',  action="store_true", default=False, help='enables log scale as default')
    args = parser.parse_args()

    main(args)
