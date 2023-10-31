"""
Generate scenarios from a folder contains multiple WAYMO data records
Author: Detian Guo
Date: 04/11/2022
"""
import argparse
import json
import os.path
import re
import time
import traceback
import itertools

from rich.progress import track
import tensorflow as tf
from helpers.create_rect_from_file import features_description, get_parsed_carla_data
from logger.logger import *
from scenario_miner import ScenarioMiner
from tags_generator import TagsGenerator
from multiprocessing import Pool
from warnings import simplefilter

simplefilter('error')

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, required=True, help='Absolute path to the data directory')
parser.add_argument('--results_dir', type=str, required=True, help='Relative path to the results')
parser.add_argument('--n_jobs', type=int, default=8, required=False, help='Number of processes')
parser.add_argument('--remake', type=bool, default=False, required=False, help='If False, it skips tagging scenes that are already in the results folder')

# working directory 
ROOT = Path(__file__).parents[1]

args = parser.parse_args()
# modify the following two lines to your own data and result directory
DATA_DIR = Path(args.data_dir)
RESULTS_DIR = Path(args.results_dir)
DATA_DIR_WALK = DATA_DIR.iterdir()


def process_scenario(data, fileprefix, FILENUM, FILE):
    try:
        parsed = tf.io.parse_single_example(data, features_description)
        scene_id = parsed['scenario/id'].numpy().item().decode("utf-8")
        print(f"Processing scene: {scene_id}.")
        result_filename = f'{fileprefix}_{FILENUM}_{scene_id}_tag.json'
        savepath = RESULT_DIR / result_filename
        if not args.remake and os.path.exists(savepath) and os.path.getsize(savepath) > 0:
            print(f"Nonempty {result_filename} found. Skipping... To re-tag, set --remake to True")
            return

        #   tagging
        tags_generator = TagsGenerator()
        general_info, \
            inter_actor_relation, \
            actors_activity, \
            actors_environment_element_intersection = tags_generator.tagging(parsed, FILE)
        result_dict = {
            'general_info': general_info,
            'inter_actor_relation': inter_actor_relation,
            'actors_activity': actors_activity,
            'actors_environment_element_intersection': actors_environment_element_intersection
        }
        with open(savepath, 'w') as f:
            print(f"Saving tags.")
            json.dump(result_dict, f)
    except Exception as e:
        trace = traceback.format_exc()
        logger.error(f"FILE:{FILENUM}.\nTag generation error:{e}")
        logger.error(f"trace:{trace}")


def process_file(DATA_PATH):
    FILE = DATA_PATH.name
    FILENUM = re.search(r"-(\d{5})-", FILE)
    if FILENUM is not None:
        FILENUM = FILENUM.group()[1:-1]
        print(f"Processing file: {FILE}.")
    else:
        print(f"File name error: {FILE}.")
        return

    fileprefix = 'Waymo'
    dataset = tf.data.TFRecordDataset(DATA_DIR / FILE, compression_type='')

    all_data = []
    all_fileprefixes = itertools.repeat(fileprefix)
    all_filenums = itertools.repeat(FILENUM)
    all_files = itertools.repeat(FILE)
    for data in dataset.as_numpy_iterator():
        all_data.append(data)

    pool = Pool(args.n_jobs)
    pool.starmap(process_scenario, zip(all_data, all_fileprefixes, all_filenums, all_files))
    pool.close()


if __name__ == '__main__':
    # RESULT_TIME = time.strftime("%Y-%m-%d-%H_%M", time.localtime())
    # RESULT_DIR = ROOT / "results" / RESULT_TIME
    RESULT_DIR = ROOT / "results" / RESULTS_DIR
    if not RESULT_DIR.exists():
        RESULT_DIR.mkdir(exist_ok=True, parents=True)
    time_start = time.perf_counter()

    for data_path in DATA_DIR_WALK:
        print("Processing ", data_path)
        process_file(data_path)

    time_end = time.perf_counter()
    print(f"Time cost: {time_end - time_start:.2f}s.RESULT_DIR: {RESULT_DIR}")
    logger.info(f"Time cost: {time_end - time_start:.2f}s.RESULT_DIR: {RESULT_DIR}")
