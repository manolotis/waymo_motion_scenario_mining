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

RESULT_PATH_GUEST = RESULT_DIR / Path("testing_guest.json")
RESULT_PATH_HOST = RESULT_DIR / Path("testing_host.json")
SCs_DIR = ROOT / SCs_DIR

scenario_index_guest = {}
scenario_index_host = {}  #
"""
scenario_index = {
    "scene_id" = {
        "agent_id": [List of SCs]
    }
}
"""

scenario_timestamp_1 = 0
scenario_timestamp_2 = 0
scenario_timestamp_5 = 0

for scenario_category_path in track(SCs_DIR.iterdir()):
    scenario_category = scenario_category_path.name

    for scenarios_json in scenario_category_path.iterdir():
        filenum = scenarios_json.name.split("_")[1]
        scene_id = scenarios_json.name.split("_")[2]
        result_dict = json.load(open(scenarios_json, 'r'))
        file_prefix = scenarios_json.name.split("_")[0]

        if scene_id not in scenario_index_guest:
            scenario_index_guest[scene_id] = {}

        if scene_id not in scenario_index_host:
            scenario_index_host[scene_id] = {}

        for i, scenario_info in result_dict.items():
            time_stamp_len = len(scenario_info['time_stamp'])
            if time_stamp_len <= 1:
                scenario_timestamp_1 += 1
            if time_stamp_len <= 2:
                scenario_timestamp_2 += 1
            if time_stamp_len <= 5:
                scenario_timestamp_5 += 5

            # For now, skip SCs that are only detected at 1 time stamp. More often than not they are noisy

            if scenario_info["guest_actor_id"] is None or scenario_info["guest_actor_id"] == 'None':
                # guest actor is none in this scenario. Add to host index
                host_actor_id = int(scenario_info["host_actor_id"])  # ID in waymo

                if host_actor_id not in scenario_index_host[scene_id]:
                    scenario_index_host[scene_id][host_actor_id] = []

                if scenario_category not in scenario_index_host[scene_id][host_actor_id]:
                    scenario_index_host[scene_id][host_actor_id].append(scenario_category)
            else:
                guest_actor_id = int(scenario_info["guest_actor_id"])  # ID in waymo

                if guest_actor_id not in scenario_index_guest[scene_id]:
                    scenario_index_guest[scene_id][guest_actor_id] = []

                if scenario_category not in scenario_index_guest[scene_id][guest_actor_id]:
                    scenario_index_guest[scene_id][guest_actor_id].append(scenario_category)

with open(RESULT_PATH_GUEST, "w") as f:
    json.dump(scenario_index_guest, f)
with open(RESULT_PATH_HOST, "w") as f:
    json.dump(scenario_index_host, f)

print("# Scenarios with 1 or less timestamps: ", scenario_timestamp_1)
print("# Scenarios with 2 or less timestamps: ", scenario_timestamp_2)
print("# Scenarios with 5 or less timestamps: ", scenario_timestamp_5)