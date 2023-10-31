import os
import time
from pathlib import Path
import numpy as np
import json
import argparse
from helpers.create_rect_from_file import get_agent_list, actor_creator, get_parsed_data, get_parsed_carla_data
from environ_elements import EnvironmentElementsWaymo
import matplotlib.pyplot as plt
# from parameters.plot_parameters import font1, font2
from parameters.plot_parameters import *
from parameters.tag_parameters import *
from plotting_scenarios import get_color_map, set_scaling_3
from helpers.diverse_plot import plot_road_lines
from collections import OrderedDict
import multiprocessing
from rich.progress import track

ROOT = Path.cwd().parent
# ToDo: parametarize
DATA_DIR = Path("/home/manolotis/sandbox/datasets/waymo_v1.0/uncompressed/tf_example/testing")
RESULTS_DIR = Path("/home/manolotis/sandbox/scenario_based_evaluation/scenario_mining/results/testing/SC")
RESULT_TIME = 'testing'
DATA = "uncompressed_tf_example_validation_validation_tfexample.tfrecord-{}-of-00150"
n_jobs = 8


# ToDo: cleanup
def plot_actor_traj(ax, actor, color, time, label: str):
    traj_x, traj_y = actor.kinematics["x"], actor.kinematics["y"]
    yaw = actor.kinematics["bbox_yaw"][time[0]]
    length, width = actor.kinematics["length"][time[0]], actor.kinematics["width"][time[0]]
    init_polygon = actor.instant_polygon(traj_x[time[0]], traj_y[time[0]], yaw, length, width)
    init_plg_x, init_plg_y = init_polygon.exterior.xy
    ax.fill(init_plg_x, init_plg_y, color=color, alpha=0.5, label=f"{label}'s initial bounding box")
    dx = traj_x[time[-1]] - traj_x[time[-2]]
    dy = traj_y[time[-1]] - traj_y[time[-2]]
    arrow = plt.arrow(traj_x[time[-2]], traj_y[time[-2]], dx, dy, width=0.3, head_width=2, color=color,
                      label=f"{label}'s trajectory")
    ax.plot(traj_x[time], traj_y[time], color=color, linewidth=4, linestyle="-")
    return ax


# ToDo: cleanup
def plot_actor_polygon(ax, fig, actor, colorbar: bool, time, label: str, fraction: float, cbo: str = "vertical"):
    actor_polygon = actor.polygon_set()
    # colors = get_color_map(ax,fig,time[0],time[-1],fraction=fraction,gradient=True,colorbar=colorbar,cborientation=cbo)
    colors = get_color_map(ax, fig, time[0], time[-1], gradient=True, colorbar=colorbar, cborientation=cbo)
    view_port = [0, 0, 0, 0]
    for step in time:
        actor_polygon_step = actor_polygon[step]
        x, y = actor_polygon_step.exterior.xy
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)
        view_port = (
            min(min_x, view_port[0]), max(max_x, view_port[1]), min(min_y, view_port[2]), max(max_y, view_port[3]))
        ax.fill(x, y, c=colors[step - time[0]])
    return ax, view_port


# ToDo: cleanup
def plot_scenario(host_actor, guest_actor, time, xlim, ylim, fraction: float, host_text, guest_text,
                  cbo: str = "vertical"):
    nrows, ncols = 1, 1
    fig, ax = plt.subplots(nrows, ncols, figsize=(15, 15))
    ax.set_aspect('equal')
    # ax,environment_element,original_data_roadgragh,original_data_light = plot_road_graph(parsed, ax)
    ##### M ax = plot_road_lines(ax, original_data_roadgragh,original_data_light,road_edge=True,road_lines=True,controlled_lane=True)
    ax = plot_road_lines(ax, original_data_roadgragh, original_data_light, road_edge=True, road_lines=True,
                         controlled_lane=True)
    ax.set_xlabel('x (m)', fontdict=font2)
    ax.set_ylabel('y (m)', fontdict=font2)
    #### M
    # def ticks(xlim,ylim):
    #     # x_ticks = np.arange(xlim[0],xlim[1],(xlim[1]-xlim[0])//5)
    #     # y_ticks = np.arange(ylim[0],ylim[1],(ylim[1]-ylim[0])//5)
    #     x_ticks = np.arange(xlim[0],xlim[1],1)
    #     y_ticks = np.arange(ylim[0],ylim[1],1)
    #     x_ticklabels = [f"{x-xlim[0]}" for x in x_ticks]
    #     x_ticklabels[0] = " "
    #     y_ticklabels = [f"{y-ylim[0]}" for y in y_ticks]
    #     return x_ticks,y_ticks, x_ticklabels, y_ticklabels
    # x_ticks,y_ticks, x_ticklabels, y_ticklabels = ticks(xlim,ylim)
    # ax.set_xticks(x_ticks,x_ticklabels,fontdict=font2)
    # ax.set_yticks(y_ticks,y_ticklabels,fontdict=font2)
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlim(xlim[0], xlim[1])
    #### M

    ax, view_port_h = plot_actor_polygon(ax, fig, host_actor, True, time, "host", fraction, cbo=cbo)
    ax, view_port_g = plot_actor_polygon(ax, fig, guest_actor, False, time, "guest", fraction, cbo=cbo)
    #### M
    # ax.text(host_text[0],host_text[1],host_text[2],
    #      fontsize=font3['size'],
    #      color="black",verticalalignment ='center',horizontalalignment ='center',
    #      bbox ={'facecolor':'white','edgecolor':None,'pad':10}
    #     )
    # ax.text(guest_text[0],guest_text[1],guest_text[2],
    #      fontsize=font3['size'],
    #      color="black",verticalalignment ='center',horizontalalignment ='center',
    #      bbox ={'facecolor':'white','edgecolor':None,'pad':10}
    #     )
    #### M
    # handels,labels = [],[]
    # ax_handels,ax_labels = ax.get_legend_handles_labels()
    # handels.extend(ax_handels)
    # labels.extend(ax_labels)
    # by_label = OrderedDict(zip(labels,handels))
    # axbox = ax.get_position()
    # ax.legend(by_label.values(),by_label.keys(),ncol=2,
    #           bbox_to_anchor=(0., 1.0, 1., 0.), loc='lower left',
    #           markerscale=15,
    #           prop=font1)

    return fig, ax


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


for sc in track(scenario_categories):
    jsons = os.listdir(RESULTS_DIR / sc)

    for json_file in jsons:
        # json_file exampole: Waymo_00100_e0da775835848d49_SC1.json
        json_path = RESULTS_DIR / sc / json_file
        _, filenum, scene_id, category = json_file.replace(".json", "").split("_")

        scene_scenarios = get_scene_scenarios(json_path)
        parsed = get_parsed_data(DATA_DIR / DATA.format(filenum), scene_id=scene_id)

        DATA_NUM = filenum

        environment_element = EnvironmentElementsWaymo(parsed)
        original_data_roadgragh, original_data_light = environment_element.road_graph_parser()

        for scenario_index, scenario_info in scene_scenarios.items():
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

            fig, ax = plot_scenario(host_actor, guest_actor, times, xlim, ylim, fraction=0.048, host_text="",
                                    guest_text="", cbo="vertical")
            # ax.ticklabel_format(style='sci',scilimits=(-1,1),axis='both')
            FIG_PATH = ROOT / "figures" / "testing"
            if not os.path.exists(FIG_PATH):
                os.makedirs(FIG_PATH)
            plt.tight_layout()
            plt.savefig(FIG_PATH / f"{sc}_{scene_id}_h{host_id}_{host_idx}_g{guest_id}_{guest_idx}.png", dpi=300)
            # plt.show()
            plt.close()
