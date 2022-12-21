# imports and global setting
import os
import time
import argparse
from plotting_scenarios import plot_all_scenarios
from logger.logger import *
from pathlib import Path


# working directory
ROOT = Path(__file__).parent.parent

argparser = argparse.ArgumentParser()

argparser.add_argument(
    '-d', '--data',
    type=str,
    help='Directory to waymo raw data',
    required=True
)

argparser.add_argument(
    '-f', '--fig',
    type=str,
    help='Directory to save figures',
    required=True
)

argparser.add_argument(
    '-r', '--result',
    type=str,
    help='Directory to save results',
    required=True
)

argparser.add_argument(
    '--filenum',
    type=str,
    required=True,
    help='#file to plot.e.g.:00003'
)
argparser.add_argument(
    '--result_time',
    type=str,
    required=True,
    help='#result time to plot.e.g.:11-09-09_25'
)

args = argparser.parse_args()

# modify the following two lines to your own data,figures, and result directory
DATADIR = args.data
FIGDIR = args.fig
RESULTDIR = args.result

if __name__ == "__main__":
    start = time.perf_counter()
    FILENUM = args.filenum
    RESULT_TIME = f"2022-{args.result_time}"
    FILE = f"training_tfexample.tfrecord-{FILENUM}-of-01000"
    RESULT_FILENAME = f'Waymo_{FILENUM}_{RESULT_TIME}_tag.json'
    RESULT_SOLO = f'Waymo_{FILENUM}_{RESULT_TIME}_solo.json'
    # sanity check
    FILENAME = os.path.join(DATADIR, FILE)
    if os.path.exists(FILENAME):
        print(f"Plotting:{FILE}")
        try:
            _ = plot_all_scenarios(DATADIR, FILE, FILENUM, RESULTDIR, RESULT_FILENAME, RESULT_SOLO, FIGDIR)
        except Exception as e:
            logger.error(f"FILE: {FILENUM}.{e}")
    else:
        print(f"File not found:{FILE}")
        logger.info(f"File not found:{FILENAME}")
    end = time.perf_counter()
    logger.info(f"DATA:{FILENUM}.JSON:{RESULT_SOLO}.Run time: {end - start}")
