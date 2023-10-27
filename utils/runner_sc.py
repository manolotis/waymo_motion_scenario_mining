import json
import traceback
import argparse
from logger.logger import *
from rich.progress import track
from scenario_categorizer import ScenarioCategorizer
import time
from multiprocessing import Pool
import itertools

# working directory
ROOT = Path(__file__).parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--result_time', type=str, required=True, help='result time to be categorized, e.g., 02-28-16_35')
parser.add_argument('--eval_mode', action="store_true", help='[bool] True for evaluation mode')
parser.add_argument('--n_jobs', type=int, default=8, required=False, help='Number of processes')
args = parser.parse_args()

RESULT_DIR = ROOT / "results" / args.result_time
file_prefix = "Waymo"

sc = ["SC1", "SC7", "SC13"]


def process_result_file(result_file, SC_ID):
    if not result_file.name.endswith("tag.json"):
        return
    filenum = result_file.name.split("_")[1]
    scenenum = result_file.name.split("_")[2]
    result_dict = json.load(open(result_file, 'r'))
    file_prefix = result_file.name.split("_")[0] if args.eval_mode else "Waymo"
    scenario_categorizer = ScenarioCategorizer(result_dict)
    try:
        SC_ID_dict = scenario_categorizer.find_SC(SC_ID)
        if not len(SC_ID_dict):
            return
        RESULT_SC_DIR = RESULT_DIR / "SC" / SC_ID
        RESULT_SC_DIR.mkdir(parents=True, exist_ok=True)
        json.dump(SC_ID_dict, open(RESULT_SC_DIR / f"{file_prefix}_{filenum}_{scenenum}_{SC_ID}.json", 'w'))
    except Exception as e:
        trace = traceback.format_exc()
        logger.error(f"SC:{SC_ID}.\nTag generation:{e}")
        logger.error(f"trace:{trace}")


def categorize_all_sc(result_dir):
    for SC_ID in track(sc, description="Categorizing..."):
        pool = Pool(args.n_jobs)
        pool.starmap(process_result_file, zip(result_dir.iterdir(), itertools.repeat(SC_ID)))
        pool.close()


if __name__ == '__main__':
    time_start = time.perf_counter()
    categorize_all_sc(RESULT_DIR)
    time_end = time.perf_counter()
    print(f"Entire run time :{(time_end - time_start):.2f}s.")
