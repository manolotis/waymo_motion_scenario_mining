import pandas as pd
from scenario_mining.utils.parameters.tags_dict import TagDict
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

utils_directory = Path(__file__).parents[1]
default_path = "/home/manolotis/sandbox/scenario_based_evaluation/scenario_mining/utils/parameters/scenario_categories.csv"
default_savepath = str(utils_directory / Path("parameters/scenario_categories.py"))
parser.add_argument('--path', type=str, required=False, default=default_path, help='Absolute path to the csv')
parser.add_argument('--savepath', type=str, required=False, default=default_savepath,
                    help='Absolute path to save generated SCs .py')
parser.add_argument('--step', type=int, required=False, default=22, help='How many rows each SC takes in the CSV')
parser.add_argument('--scenarios-column', type=int, required=False, default=0, help='Index of scenarios column')
parser.add_argument('--sections-column', type=int, required=False, default=1, help='Index of sections column')
parser.add_argument('--categories-column', type=int, required=False, default=2, help='Index of categories column')
parser.add_argument('--tags-column', type=int, required=False, default=3, help='Index of tags column')
parser.add_argument('--values-column', type=int, required=False, default=4, help='Index of values column')

args = parser.parse_args()

df = pd.read_csv(args.path, header=None)
step = args.step
scenarios_column = args.scenarios_column
sections_column = args.sections_column
categories_column = args.categories_column
tags_column = args.tags_column
values_column = args.values_column


class ScenarioDefinition:

    def __init__(self, df, row):
        #####   general info    #####
        self.import_general_info(df, row)

        #####   host actor  #####
        self.import_host_actor_info(df, row + 5)

        #####   guest actor  #####
        self.import_guest_actor_info(df, row + 13)

        self.import_envr_info(df, row + 21)

        self.validate_data()

    def import_general_info(self, df, row):
        self.SC_ID = df[values_column][row]
        self.description = df[values_column][row + 1]
        self.source = df[values_column][row + 2]
        self.source_file = df[values_column][row + 3]
        self.notes = df[values_column][row + 4]

    def import_envr_info(self, df, row):
        self.envr_tag = {
            "light_state": df[values_column][row]
        }

    def import_host_actor_info(self, df, row):
        self.host_actor_type = self.import_list(df, row)
        self.host_actor_tag: dict = {
            "lo_act": self.import_list(df, row + 1),
            "la_act": self.import_list(df, row + 2),
            "road_relation": self.import_list(df, row + 3),
            "road_type": self.import_list(df, row + 4),
            "inter_actor_relation": self.import_list(df, row + 5),
            "inter_actor_position": self.import_list(df, row + 6),
            'inter_actor_heading': self.import_list(df, row + 7),
        }

    def import_guest_actor_info(self, df, row):
        self.guest_actor_type = self.import_list(df, row)
        self.guest_actor_tag: dict = {
            "lo_act": self.import_list(df, row + 1),
            "la_act": self.import_list(df, row + 2),
            "road_relation": self.import_list(df, row + 3),
            "road_type": self.import_list(df, row + 4),
            "inter_actor_relation": self.import_list(df, row + 5),
            "inter_actor_position": self.import_list(df, row + 6),
            'inter_actor_heading': self.import_list(df, row + 7),
        }

    def import_list(self, df, row):
        value = df[values_column][row].lower()
        if value == "-" or value == "":
            return []
        # remove
        value = value.replace("'", "")
        value = value.replace('"', "")
        value_list = [value.strip() for value in value.split(",")]
        # value_list = [value.replace(" ", "_") for value in value_list]
        return value_list

    def format_list(self, items):
        return items  # in case we want to do some extra formatting

    def validate_actor_type(self, actor_type):
        for t in actor_type:
            assert t in ["vehicle", "pedestrian", "cyclist"], f"Actor type {t} not found"

    def validate_actor_tags(self, actor_tags):
        for k in actor_tags.keys():
            # assert k in TagDict.keys(), f"Tag type {k} not found in TagDict"
            for tag in actor_tags[k]:
                # road type not explictly included
                if k == "road_type":
                    continue
                assert tag in TagDict[
                    k].values(), f"Tag value {tag} not found in TagDict of type[{k}]. Values found: {TagDict[k].values()}"

    def validate_data(self):
        # make sure we only have values that are allowed

        assert isinstance(self.SC_ID, str)
        assert isinstance(self.description, str)
        assert isinstance(self.source, str)
        assert isinstance(self.source_file, str)
        assert isinstance(self.notes, str)

        self.validate_actor_tags(self.host_actor_tag)
        self.validate_actor_tags(self.guest_actor_tag)

        self.validate_actor_type(self.host_actor_type)
        self.validate_actor_type(self.guest_actor_type)

    def tostring(self):
        string = f"""
@dataclass
class {self.SC_ID}(SCBasis):
    #####   general info    #####
    SC_ID = "{self.SC_ID}"
    description = "{self.description}"
    source = "{self.source}"
    source_file = "{self.source_file}"
    notes = '''
    {self.notes}
    '''
    #####   host actor  #####
    host_actor_type = {self.format_list(self.host_actor_type)}
    host_actor_tag = {{
        "lo_act": {self.format_list(self.host_actor_tag["lo_act"])},
        "la_act": {self.format_list(self.host_actor_tag["la_act"])},
        "road_relation": {self.format_list(self.host_actor_tag["road_relation"])},
        "road_type": {self.format_list(self.host_actor_tag["road_type"])},
        "inter_actor_relation": {self.format_list(self.host_actor_tag["inter_actor_relation"])},
        "inter_actor_position": {self.format_list(self.host_actor_tag["inter_actor_position"])},
        'inter_actor_heading': {self.format_list(self.host_actor_tag["inter_actor_heading"])},
    }}
    #####   guest actor  #####
    guest_actor_type = {self.format_list(self.guest_actor_type)}
    guest_actor_tag = {{
        "lo_act": {self.format_list(self.guest_actor_tag["lo_act"])},
        "la_act": {self.format_list(self.guest_actor_tag["la_act"])},
        "road_relation": {self.format_list(self.guest_actor_tag["road_relation"])},
        "road_type": {self.format_list(self.guest_actor_tag["road_type"])},
        "inter_actor_relation": {self.format_list(self.guest_actor_tag["inter_actor_relation"])},
        "inter_actor_position": {self.format_list(self.guest_actor_tag["inter_actor_position"])},
        'inter_actor_heading': {self.format_list(self.guest_actor_tag["inter_actor_heading"])},
    }}


"""
        return string

    @staticmethod
    def get_top_string():
        return """
# dataclasses for scenario categories
# Author: Manuel Muñoz Sánchez
# Date: 2023-10-27

from dataclasses import dataclass


class SCBasis:
    ''' 
    This is the basis for all scenario categories.
    The dictionary of host/guest_actor_tag overwritten by the child class.
     
    value dimensions:
    [..., ] -> the options of tag
    [[..., ], [..., ]] -> the consequent options of tags
    '''

    #####   general info    #####
    SC_ID: str = "SC_0"
    description = "This is the basis for all scenario categories."
    source: str = ""
    source_file: str = ""
    #####   host actor  #####
    host_actor_type = []
    host_actor_tag: dict = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag: dict = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    envr_tag = {
        'light_state': []
    }
"""

    @staticmethod
    def get_scenario_catalog(scenario_ids):
        string = "scenario_catalog = {\n"
        for sc_id in scenario_ids:
            string += f"    '{sc_id}': {sc_id},\n"
        string += "}\n"
        return string


def get_scenario_ids():
    scenario_ids = []
    for r in range(0, 999, 22):
        try:
            sc_id = df[scenarios_column][r]
        except ValueError:  # finished file
            break
        if sc_id == "SCX":
            break
        scenario_ids.append(sc_id)

    return scenario_ids


def get_scenario_indexes():
    scenario_indexes = []
    for r in range(0, 999999, 22):
        try:
            sc_id = df[scenarios_column][r]
        except ValueError:  # finished file
            break
        if sc_id == "SCX":
            break
        scenario_indexes.append(r)

    return scenario_indexes


if __name__ == "__main__":
    scenario_categories_file = ""
    scenario_categories_file += ScenarioDefinition.get_top_string()

    scenario_ids = get_scenario_ids()

    for i, scenario_index in enumerate(get_scenario_indexes()):
        print(f"Importing scenario {scenario_ids[i]}, starting row {scenario_index}")
        scenario_definition = ScenarioDefinition(df, scenario_index)
        scenario_categories_file += scenario_definition.tostring()

    scenario_categories_file += ScenarioDefinition.get_scenario_catalog(scenario_ids)

    with open(args.savepath, "w") as f:
        f.write(scenario_categories_file)
