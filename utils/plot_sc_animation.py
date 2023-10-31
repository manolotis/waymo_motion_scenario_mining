import os
from pathlib import Path
import json
from helpers.create_rect_from_file import get_agent_list, actor_creator, get_parsed_data, get_parsed_carla_data
from environ_elements import EnvironmentElementsWaymo
import matplotlib.pyplot as plt
from parameters.plot_parameters import *
from parameters.tag_parameters import *
from plotting_scenarios import get_color_map, set_scaling_3
from helpers.diverse_plot import plot_road_lines
from rich.progress import track
import matplotlib.animation as animation

ROOT = Path.cwd().parent
# ToDo: parametarize
DATA_DIR = Path("/home/manolotis/sandbox/datasets/waymo_v1.0/uncompressed/tf_example/testing")
RESULTS_DIR = Path("/home/manolotis/sandbox/scenario_based_evaluation/scenario_mining/results/testing/SC")
RESULT_TIME = 'testing'
DATA = "uncompressed_tf_example_validation_validation_tfexample.tfrecord-{}-of-00150"
n_jobs = 8


# ToDo: cleanup

def get_bbox(ax, fig, actor, time, cbo, t):
    actor_polygon = actor.polygon_set()
    colors = get_color_map(ax, fig, time[0], time[0] + 1, gradient=True, colorbar=False, cborientation=cbo)
    actor_polygon_step = actor_polygon[t]
    x, y = actor_polygon_step.exterior.xy
    # bbox = ax.fill(x, y, c=colors[0])
    bbox = ax.fill(x, y, c="tab:blue")
    return bbox


def plot_scenario(host_actor, guest_actor, time, xlim, ylim, fraction: float, host_text, guest_text,
                  cbo: str = "vertical"):
    nrows, ncols = 1, 1
    fig, ax = plt.subplots(nrows, ncols, figsize=(10, 10))
    ax.set_xlabel('x (m)', fontdict=font1)
    ax.set_ylabel('y (m)', fontdict=font1)
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlim(xlim[0], xlim[1])

    ax.set_aspect('equal')
    artists = []

    for i, t in enumerate(time):
        _, road = plot_road_lines(ax, original_data_roadgragh, original_data_light, road_edge=True, road_lines=True,
                                  controlled_lane=True, return_artists=True)

        bboxes = []
        bboxes.extend(get_bbox(ax, fig, host_actor, time, cbo, t))
        bboxes.extend(get_bbox(ax, fig, guest_actor, time, cbo, t))

        artists.append(road + bboxes)
        # plt.show()
        # plt.close()

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=100, blit=True)
    return ani


scenario_categories = os.listdir(RESULTS_DIR)
sc2types = {
    "SC1": {
        "host_type": 1,
        "guest_type": 1,
    },
    "SC7": {
        "host_type": 1,
        "guest_type": 2,
    },
    "SC13": {
        "host_type": 1,
        "guest_type": 3,
    }
}


def get_scene_scenarios(json_path):
    with open(json_path, "r") as f:
        scene_scenarios = json.load(f)

    return scene_scenarios


for sc in sorted(scenario_categories, reverse=True):
    print("Processing", sc)
    jsons = os.listdir(RESULTS_DIR / sc)

    for json_file in track(jsons):
        # json_file exampole: Waymo_00100_e0da775835848d49_SC1.json
        json_path = RESULTS_DIR / sc / json_file
        _, filenum, scene_id, category = json_file.replace(".json", "").split("_")

        scene_scenarios = get_scene_scenarios(json_path)
        parsed = get_parsed_data(DATA_DIR / DATA.format(filenum), scene_id=scene_id)

        DATA_NUM = filenum

        environment_element = EnvironmentElementsWaymo(parsed)
        original_data_roadgragh, original_data_light = environment_element.road_graph_parser()

        for scenario_index, scenario_info in scene_scenarios.items():
            print(f"processing {json_file}, scenario index {scenario_index}")
            host_id, guest_id = int(scenario_info["host_actor"]), int(scenario_info["guest_actor"])
            host_idx, guest_idx = int(scenario_info["host_actor_id"]), int(scenario_info["guest_actor_id"])
            host_actor, _ = actor_creator(sc2types[sc]["host_type"], host_id, parsed)
            guest_actor, _ = actor_creator(sc2types[sc]["guest_type"], guest_id, parsed)

            valid_times_host = np.argwhere(host_actor.validity > 0).flatten()
            valid_times_guest = np.argwhere(guest_actor.validity > 0).flatten()
            valid_x_host = host_actor.kinematics['x'][valid_times_host]
            valid_y_host = host_actor.kinematics['y'][valid_times_host]
            valid_x_guest = guest_actor.kinematics['x'][valid_times_guest]
            valid_y_guest = guest_actor.kinematics['y'][valid_times_guest]

            valid_times_both = set(list(valid_times_host) + list(valid_times_guest))
            times = np.array(sorted(valid_times_both))

            # delta = 50

            x_min = np.concatenate([valid_x_host, valid_x_guest]).min() - 5
            x_max = np.concatenate([valid_x_host, valid_x_guest]).max() + 5
            y_min = np.concatenate([valid_y_host, valid_y_guest]).min() - 5
            y_max = np.concatenate([valid_y_host, valid_y_guest]).max() + 5

            x_range = x_max - x_min
            y_range = y_max - y_min
            diff = np.abs(y_range - x_range)
            padding = diff / 2
            xlim = (x_min, x_max)
            ylim = (y_min, y_max)

            # make sure we keep square-ish ratio
            if x_range >= y_range:
                ylim = (y_min - padding, y_max + padding)
            elif y_range > x_range:
                xlim = (x_min - padding, x_max + padding)

            # fig, ax = plot_scenario(host_actor, guest_actor, times, xlim, ylim, fraction=0.048, host_text="",
            #                         guest_text="", cbo="vertical")

            FIG_DIR = ROOT / "figures" / "testing_animation"
            if not os.path.exists(FIG_DIR):
                os.makedirs(FIG_DIR)
            FIG_PATH = FIG_DIR / f"{sc}_{scene_id}_h{host_id}_{host_idx}_g{guest_id}_{guest_idx}.gif"

            if os.path.exists(FIG_PATH) and os.path.getsize(FIG_DIR) > 0: # skip if already exists
                continue

            ani = plot_scenario(host_actor, guest_actor, times, xlim, ylim, fraction=0.048, host_text="",
                                guest_text="", cbo="vertical")


            plt.tight_layout()
            # plt.savefig(FIG_PATH / f"{sc}_{scene_id}_h{host_id}_{host_idx}_g{guest_id}_{guest_idx}.png", dpi=300)
            # plt.show()



            # ani.save(filename=FIG_PATH, writer="pillow", progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'), dpi=200)
            ani.save(filename=FIG_PATH, writer="pillow", dpi=200)

            plt.close()
