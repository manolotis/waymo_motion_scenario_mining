# imports and global setting

import argparse
import time
import traceback
from pathlib import Path

from logger.logger import *
from plotting_scenarios import plot_all_scenarios

# working directory
ROOT = Path(__file__).parent.parent

# modify the following two lines to your own data,figures, and result directory
DATADIR = ROOT / "waymo_open_dataset" / "data" / "tf_example" / "training"
FIGDIR = ROOT / "figures" / "scenarios" / "eval"
RESULTDIR = ROOT / "results" / "gp1"

parser = argparse.ArgumentParser()
parser.add_argument('--filenum', type=str, required=True, help='#file to plot.e.g.:00003')
parser.add_argument('--result_time', type=str, required=True, help='#result time to plot.e.g.:11-09-09_25')
parser.add_argument('--eval_mode', type=bool, required=False, default=False ,help='[bool] True for evaluation mode')
args = parser.parse_args()
eval_mode = args.eval_mode
if eval_mode:
    DATADIR = ROOT / "waymo_open_dataset" / "data" / "eval_data" / "carla_data"


if __name__ == "__main__":
    start = time.perf_counter()
    FILENUM = args.filenum
    RESULT_TIME = f"2023-{args.result_time}"
    FILE = f"training_tfexample.tfrecord-{FILENUM}-of-01000"
    RESULT_FILENAME = f'Waymo_{FILENUM}_{RESULT_TIME}_tag.json'
    RESULT_SOLO = f'Waymo_{FILENUM}_{RESULT_TIME}_solo.json'
    if eval_mode:
        FILE = f"PedestrianCrossing-{FILENUM}-of-00000.pkl"
        RESULT_FILENAME = f'Carla_{FILENUM}_{RESULT_TIME}_tag.json'
        RESULT_SOLO = f'Carla_{FILENUM}_{RESULT_TIME}_solo.json'
    # sanity check
    FILE_PATH = DATADIR / FILE
    if FILE_PATH.exists():
        print(f"Plotting:{FILE}")
        try:
            _=plot_all_scenarios(DATADIR,FILE,FILENUM,RESULTDIR / RESULT_TIME,RESULT_FILENAME,RESULT_SOLO,FIGDIR,eval_mode=eval_mode)
        except Exception as e:
            ##########################################
            # messager for finishing one data record. Comment out this if you don't use wechat
            # wechatter(f"Error in plotting {FILENUM}")
            ##########################################
            trace = traceback.format_exc()
            logger.error(f"FILE: {FILENUM}.{e}")
            logger.error(f"trace:{trace}")
    else:
        print(f"File not found:{FILE}")
        logger.info(f"File not found:{FILE_PATH}")
    end = time.perf_counter()
    logger.info(f"DATA:{FILENUM}.JSON:{RESULT_SOLO}.Run time: {end-start}")

    # messager for finishing using wechat. Comment out this if you don't want to use wechat
    # wechatter(f"{FILENUM} Plot finished. Run time: {end-start}")

