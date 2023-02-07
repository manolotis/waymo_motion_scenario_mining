# imports and global setting
import os
import time
import argparse
from plotting_scenarios import plot_all_scenarios
from logger.logger import *
from pathlib import Path
import glob

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


def get_all_file_numbers(args):
    file_numbers = []
    file_paths = glob.glob(f"{args.result}*_solo.json")
    for file in file_paths:
        file_number = file.split("_")[1]
        file_numbers.append(file_number)

    # Should not happen, but just make sure we don't have duplicates
    numbers_set = set(file_numbers)
    file_numbers = list(sorted(numbers_set))

    return file_numbers


if __name__ == "__main__":

    RESULT_TIME = f"{args.result_time}"

    if args.filenum == "all":
        file_numbers = get_all_file_numbers(args)
        print("Filenumbers", file_numbers)
    else:
        file_numbers = [args.file_number]

    for file_number in file_numbers:
        start = time.perf_counter()
        if "train" in args.data:
            FILE = f"training_tfexample.tfrecord-{file_number}-of-01000"
        else:
            FILE = f"validation_tfexample.tfrecord-{file_number}-of-00150"

        RESULT_FILENAME = f'Waymo_{file_number}_{RESULT_TIME}_tag.json'
        RESULT_SOLO = f'Waymo_{file_number}_{RESULT_TIME}_solo.json'
        # sanity check
        FILENAME = os.path.join(DATADIR, FILE)
        print("attempting ", FILENAME)
        if os.path.exists(FILENAME):
            print(f"Plotting:{FILE}")
            try:
                _ = plot_all_scenarios(DATADIR, FILE, file_number, RESULTDIR, RESULT_FILENAME, RESULT_SOLO, FIGDIR)

            except Exception as e:
                print(e)
                raise e
                logger.error(f"FILE: {file_number}.{e}")
        else:
            print(f"File not found:{FILE}")
            print(f"Filename not found:{FILENAME}")

            logger.info(f"File not found:{FILENAME}")
        end = time.perf_counter()
        logger.info(f"DATA:{file_number}.JSON:{RESULT_SOLO}.Run time: {end - start}")
