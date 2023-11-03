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
from parameters.scenario_categories import scenario_catalog

ROOT = Path.cwd().parent
# ToDo: parametarize
DATA_DIR = Path("/home/manolotis/sandbox/datasets/waymo_v1.0/uncompressed/tf_example/testing")
RESULTS_DIR = Path("/home/manolotis/sandbox/scenario_based_evaluation/scenario_mining/results/testing/SC")
RESULT_TIME = 'testing'
DATA = "uncompressed_tf_example_validation_validation_tfexample.tfrecord-{}-of-00150"
n_jobs = 8


# ToDo: cleanup

def get_bbox(ax, fig, actor, time, cbo, t, color="tab:gray"):
    actor_polygon = actor.polygon_set()
    colors = get_color_map(ax, fig, time[0], time[0] + 1, gradient=True, colorbar=False, cborientation=cbo)
    actor_polygon_step = actor_polygon[t]
    x, y = actor_polygon_step.exterior.xy
    # bbox = ax.fill(x, y, c=colors[0])
    bbox = ax.fill(x, y, c=color)
    return bbox


def plot_scenario(parsed, host_actor, guest_actor, time, xlim, ylim, fraction: float, host_text, guest_text,
                  cbo: str = "vertical"):
    actor_types = parsed['state/type'].numpy()
    actor_idxs = np.argwhere(parsed['state/type'].numpy() > -1).flatten()
    ego_idx = np.argwhere(parsed['state/is_sdc'].numpy() > 0).flatten()[0]
    ego_id = parsed['state/id'].numpy()[ego_idx]

    nrows, ncols = 1, 1
    fig, ax = plt.subplots(nrows, ncols, figsize=(10, 10))
    ax.set_xlabel('x (m)', fontdict=font1)
    ax.set_ylabel('y (m)', fontdict=font1)
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlim(xlim[0], xlim[1])

    ax.set_aspect('equal')
    artists = []

    all_actors = []

    for actor_idx in actor_idxs:
        actor, _ = actor_creator(int(actor_types[actor_idx]), actor_idx, parsed)
        all_actors.append(actor)

    for i, t in enumerate(time):
        _, road = plot_road_lines(ax, original_data_roadgragh, original_data_light, road_edge=True, road_lines=True,
                                  controlled_lane=True, return_artists=True)

        bboxes = []

        for actor in all_actors:
            if actor.id == host_actor.id or (guest_actor is not None and actor.id == guest_actor.id):
                continue

            visible = False

            if actor.id == ego_id:
                bbox = get_bbox(ax, fig, actor, time, cbo, t, color="tab:blue")
            else:
                bbox = get_bbox(ax, fig, actor, time, cbo, t, color="lightgrey")
            # check if any point is within bounds, otherwise skip drawing it
            for patch in bbox:
                if visible:
                    break
                for (x, y) in patch.xy:
                    if x > xlim[0] and x < xlim[1] and y > ylim[0] and y < ylim[1]:
                        visible = True
                        break

            if visible:
                bboxes.extend(bbox)

        bboxes.extend(get_bbox(ax, fig, host_actor, time, cbo, t, color="tab:orange"))
        if guest_actor is not None:
            bboxes.extend(get_bbox(ax, fig, guest_actor, time, cbo, t, color="tab:orange"))

        artists.append(road + bboxes)
        # plt.show()
        # plt.close()

    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=100, blit=True)
    return ani


scenario_categories = os.listdir(RESULTS_DIR)

actor_string2actor_int = {
    "vehicle": 1,
    "pedestrian": 2,
    "cyclist": 3,
}

sc2types = {}
for sc in scenario_catalog.keys():
    sc2types[sc] = {
        "host_type": actor_string2actor_int[scenario_catalog[sc].host_actor_type[0]],
        # !watch out, this only works if 1 actor type specified
    }
    if len(scenario_catalog[sc].guest_actor_type) > 0:
        sc2types[sc] = {
            "guest_type": actor_string2actor_int[scenario_catalog[sc].guest_actor_type[0]]
            # !watch out, this only works if 1 actor type specified
        }


def get_scene_scenarios(json_path):
    with open(json_path, "r") as f:
        scene_scenarios = json.load(f)

    return scene_scenarios


# for sc in ['SC21', 'SC22', 'SC19', 'SC20'] + sorted(scenario_categories, reverse=True):
for sc in ['SC20'] + sorted(scenario_categories, reverse=True):
    print("Processing", sc)
    jsons = os.listdir(RESULTS_DIR / sc)

    for json_file in track(jsons):
        json_path = RESULTS_DIR / sc / json_file
        _, filenum, scene_id, category = json_file.replace(".json", "").split("_")

        scene_scenarios = get_scene_scenarios(json_path)
        parsed = get_parsed_data(DATA_DIR / DATA.format(filenum), scene_id=scene_id)

        DATA_NUM = filenum

        environment_element = EnvironmentElementsWaymo(parsed)
        original_data_roadgragh, original_data_light = environment_element.road_graph_parser()

        for scenario_index, scenario_info in scene_scenarios.items():
            print(f"processing {json_file}, scenario index {scenario_index}")

            host_id = int(scenario_info["host_actor"])
            host_idx = int(scenario_info["host_actor_id"])
            host_actor, _ = actor_creator(sc2types[sc]["host_type"], host_id, parsed)
            valid_times_host = np.argwhere(host_actor.validity > 0).flatten()
            valid_x_host = host_actor.kinematics['x'][valid_times_host]
            valid_y_host = host_actor.kinematics['y'][valid_times_host]

            try:
                guest_id = int(scenario_info["guest_actor"])
                guest_idx = int(scenario_info["guest_actor_id"])
                guest_actor, _ = actor_creator(sc2types[sc]["guest_type"], guest_id, parsed)
                valid_times_guest = np.argwhere(guest_actor.validity > 0).flatten()
                valid_x_guest = guest_actor.kinematics['x'][valid_times_guest]
                valid_y_guest = guest_actor.kinematics['y'][valid_times_guest]
                valid_times_both = set(list(valid_times_host) + list(valid_times_guest))
                times = np.array(sorted(valid_times_both))
                x_min = np.concatenate([valid_x_host, valid_x_guest]).min() - 5
                x_max = np.concatenate([valid_x_host, valid_x_guest]).max() + 5
                y_min = np.concatenate([valid_y_host, valid_y_guest]).min() - 5
                y_max = np.concatenate([valid_y_host, valid_y_guest]).max() + 5
            except ValueError:  # no guest actor
                guest_id = None
                guest_idx = None
                guest_actor = None
                times = np.array(sorted(list(valid_times_host)))
                x_min = valid_x_host.min() - 5
                x_max = valid_x_host.max() + 5
                y_min = valid_y_host.min() - 5
                y_max = valid_y_host.max() + 5

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

            FIG_DIR = ROOT / "figures" / "testing_animation_all_rus"
            if not os.path.exists(FIG_DIR):
                os.makedirs(FIG_DIR)
            FIG_PATH = FIG_DIR / f"{sc}_{scene_id}_h{host_id}_{host_idx}_g{guest_id}_{guest_idx}.gif"

            if os.path.exists(FIG_PATH) and os.path.getsize(FIG_DIR) > 0:  # skip if already exists
                continue

            ani = plot_scenario(parsed, host_actor, guest_actor, times, xlim, ylim, fraction=0.048, host_text="",
                                guest_text="", cbo="vertical")

            plt.tight_layout()
            # plt.show()

            # ani.save(filename=FIG_PATH, writer="pillow", progress_callback = lambda i, n: print(f'Saving frame {i}/{n}'), dpi=200)
            ani.save(filename=FIG_PATH, writer="pillow", dpi=200)

            plt.close()
