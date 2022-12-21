"""
Generate scenarios from a folder contains multiple WAYMO data records
Author: Detian Guo
Date: 04/11/2022

Some extra additions by Manuel Muñoz Sánchez on 21/12/2022 to run on entire dataset
"""
import os
import time
import re
import json
import argparse
from tags_generation import generate_tags
from mining_scenarios import mine_solo_scenarios
# from rich.progress import track
from logger.logger import *
import traceback
import argparse
from multiprocessing import Pool

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
    '-r', '--result',
    type=str,
    help='Directory to save results',
    required=True
)
argparser.add_argument(
    '-n', '--n-jobs',
    type=int,
    help='Number of processes',
    default=4
)
args = argparser.parse_args()


# modify the following two lines to your own data and result directory
DATADIR = Path(args.data)
RESULTDIR = Path(args.result)

if not os.path.exists(RESULTDIR):
    os.makedirs(RESULTDIR, exist_ok=True)

DATADIR_WALK = DATADIR.iterdir()
RESULT_TIME = time.strftime("%Y-%m-%d-%H_%M", time.localtime())

# parameters default setting
# parameter for estimation of the actor approaching a static element
TTC_1 = 5
# parameter for estimation of two actors' interaction
TTC_2 = 9


def process_file(DATA_PATH):
    FILE = DATA_PATH.name
    FILENUM = re.search(r"-(\d{5})-", FILE)
    if FILENUM is not None:
        FILENUM = FILENUM.group()[1:-1]
        print(f"Processing file: {FILE}")
    else:
        print("!!!")
        raise ValueError(f"Found some error. File {FILE}, filenum {FILENUM}")

    # return

    result_dict = {}
    RESULT_FILENAME = f'Waymo_{FILENUM}_{RESULT_TIME}_tag.json'
    try:
        print("\t", FILE, "Generating tags...")
        actors_list, \
            inter_actor_relation, \
            actors_activity, \
            actors_static_element_intersection = generate_tags(DATADIR, FILE)
        result_dict = {
            'actors_list': actors_list,
            'inter_actor_relation': inter_actor_relation,
            'actors_activity': actors_activity,
            'actors_static_element_intersection': actors_static_element_intersection
        }
        with open(os.path.join(RESULTDIR, RESULT_FILENAME), 'w') as f:
            json.dump(result_dict, f)
        # with open(os.path.join(RESULTDIR,RESULT_FILENAME.replace('.json','.pkl')),'wb') as f:
        #     pickle.dump(result_dict,f)
        print("\t", FILE, "Mining solo scenarios...")
        solo_scenarios = mine_solo_scenarios(result_dict)
        RESULT_FILENAME = f'Waymo_{FILENUM}_{RESULT_TIME}_solo.json'
        with open(os.path.join(RESULTDIR, RESULT_FILENAME), 'w') as f:
            json.dump(solo_scenarios, f)
    except Exception as e:
        trace = traceback.format_exc()
        logger.error(f"FILE:{FILENUM}.\nTag generation:{e}")
        logger.error(f"trace:{trace}")

if __name__ == '__main__':
    time_start = time.perf_counter()
    pool = Pool(args.n_jobs)
    processes = []

    # for DATA_PATH in DATADIR_WALK:
    #     process_file(DATA_PATH)
    pool.map(process_file, DATADIR_WALK)
    pool.close()




    time_end = time.perf_counter()
    print(f"Time cost: {time_end - time_start:.2f}s.RESULTDIR: {RESULTDIR}")
    logger.info(f"Time cost: {time_end - time_start:.2f}s.RESULTDIR: {RESULTDIR}")
