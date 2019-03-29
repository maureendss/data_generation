import argparse
import sys
import os
import random

def handle_arguments(cl_arguments):
    parser = argparse.ArgumentParser(description='')
    # Configuration files

    parser.add_argument('--number_runs', '-n', type=str,
                        help="Number of runs to generate")
    parser.add_argument('--slurm_dir', '-s', type=str,
                        help="Location where slurm scripts go")
    parser.add_argument('--data_dir', '-d', type=str,
                        help="Data directory ABOVE CoLA directory")
    parser.add_argument('--output_dir', '-o', type=str,
                        help="Location of output, where experiment name directory is created")
    parser.add_argument('--config_file', '-c', type=str, default="$JIANT_PROJECT_PREFIX/config/bert_tasks.conf",
                        help="location of config file")
    parser.add_argument('--exp_name', '-x', type=str,
                        help="Name of the experiment, i.e. directory name where all runs are contained")
    parser.add_argument('--max_epochs', '-e', type=str, default=10,
                        help="Maximum number of epochs")
    parser.add_argument('--lr', '-l', type=str, default="1E-5",
                        help="Learning rate")
    parser.add_argument('--val_interval', '-v', type=str, default="100",
                        help="How many batches between validation stages")
    return parser.parse_args(cl_arguments)

header = """#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=7
#SBATCH --gres=gpu:p40:1
#SBATCH --mem=16GB
#SBATCH -t24:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

#PRINCE PRINCE_GPU_COMPUTE_MODE=default

# Run.\n"""


if __name__ == '__main__':
    args = handle_arguments(sys.argv[1:])
    experiment_dir = os.path.join(os.getcwd(), args.exp_name) if args.slurm_dir is None else args.slurm_dir
    if not os.path.isdir(experiment_dir):
        os.mkdir(experiment_dir)
    for i in range(int(args.number_runs)):
        slurm_file = os.path.join(experiment_dir, "run_%d.sbatch" % i)
        out_file = open(slurm_file, "w")
        out_file.write(header)
        out_file.write("export JIANT_DATA_DIR=%s\n" % args.data_dir )
        out_file.write("export NFS_PROJECT_PREFIX=%s\n" % args.output_dir)
        out_file.write("python $JIANT_PROJECT_PREFIX/main.py --config_file " + args.config_file)
        out_file.write("--overrides \"run_name=run_" + str(i))
        out_file.write(" max_epochs=" + args.max_epochs)
        out_file.write(" lr=" + args.lr)
        out_file.write(" val_interval=" + args.val_interval)
        out_file.write(" exp_name=" + args.exp_name)
        out_file.write(" random_seed=" + str(random.randint(1000, 10000)))
        out_file.write("\"")


"""
python -m sbatch_generator -n 20 -d ~/jiant/data_generation_outputs/structure_dependence/polar_q/ \
    -o /scratch/asw462/jiant/structure_dependence/polar_q/ \
    -x polar_q_1k -e 15 -l 0.00001 -v 100
"""







#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=7
#SBATCH --gres=gpu:p40:1
#SBATCH --mem=16GB
#SBATCH -t24:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

#PRINCE PRINCE_GPU_COMPUTE_MODE=default

# Run.
#
# export JIANT_DATA_DIR=~/jiant/data_generation_outputs/structure_dependence/reflexive/3_20-5k
# export NFS_PROJECT_PREFIX=/scratch/asw462/jiant/structure_dependence/reflexive/
#
# python     ../main.py     \
# --config_file ../config/bert_tasks.conf     \
# --overrides "run_name=refl_14, max_epochs=15, lr=7E-6, val_interval=100, exp_name=refl"