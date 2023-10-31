import argparse
import os.path

from rich.progress import track
from pathlib import Path
import json

# parser = argparse.ArgumentParser()
# parser.add_argument('--data_dir', type=str, required=True, help='Absolute path to the data directory')
# parser.add_argument('--results_dir', type=str, required=True, help='Relative path to the results')
# parser.add_argument('--n_jobs', type=int, default=8, required=False, help='Number of processes')
# args = parser.parse_args()

# ToDo: multiprocessing
# ToDo: parameterize
SCs_DIR = Path("results/testing/SC")
ROOT = Path(__file__).parents[0]  # working directory
RESULT_DIR = ROOT / Path("results/index/")
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

RESULT_PATH = RESULT_DIR / Path("testing.json")
SCs_DIR = ROOT / SCs_DIR

scenario_index = {}
"""
scenario_index = {
    "scene_id" = {
        "agent_id": [List of SCs]
    }
}
"""

for scenario_category_path in track(SCs_DIR.iterdir()):
    scenario_category = scenario_category_path.name

    for scenarios_json in scenario_category_path.iterdir():
        filenum = scenarios_json.name.split("_")[1]
        scene_id = scenarios_json.name.split("_")[2]
        result_dict = json.load(open(scenarios_json, 'r'))
        file_prefix = scenarios_json.name.split("_")[0]

        if scene_id not in scenario_index:
            scenario_index[scene_id] = {}

        for i, scenario_info in result_dict.items():
            guest_actor_id = int(scenario_info["guest_actor_id"]) # ID in waymo

            if guest_actor_id not in scenario_index[scene_id]:
                scenario_index[scene_id][guest_actor_id] = []

            if scenario_category not in scenario_index[scene_id][guest_actor_id]:
                scenario_index[scene_id][guest_actor_id].append(scenario_category)

with open(RESULT_PATH, "w") as f:
    json.dump(scenario_index, f)
