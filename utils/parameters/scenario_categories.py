# dataclasses for scenario categories
# Author: Detian Guo
# Date: 2023-02-21 

from dataclasses import dataclass


class SCBasis():
    """
    This is the basis for all scenario categories.
    The dictionary of host/guest_actor_tag overwritten by the child class.
    """
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


@dataclass
class Car2CarFrontTurnLeft(SCBasis):
    """
    value dimensions:
    [..., ] -> the options of tag
    [[..., ], [..., ]] -> the consequent options of tags
    """
    #####   general info    #####
    SC_ID = "SC1"
    description = "Car-to-car_front_turn_across_path"
    source = "EURO_NCAP_2023"
    source_file = "https://cdn.euroncap.com/media/77302/euro-ncap-aeb-c2c-test-protocol-v42.pdf"
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning left'],
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', "close proximity", "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite']
    }
    #####   guest actor  #####
    guest_actor_type = ["vehicle"]
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': []
    }


@dataclass
class Car2CycFrontTurnLeft(Car2CarFrontTurnLeft):
    """
    Inherit from Car2CarFrontTurn
    """
    #####   general info    #####
    SC_ID = "SC5"
    #####   guest actor  #####
    guest_actor_type = ["cyclist"]


@dataclass
class Car2PedFrontTurnLeft(Car2CarFrontTurnLeft):
    #####   general info    #####
    SC_ID = "SC8"
    #####   guest actor  #####
    guest_actor_type = ["pedestrian"]


@dataclass
class Car2CarFrontHeadon(SCBasis):
    #####   general info    #####
    SC_ID = "SC3"
    description = "Car-to-car_front_headon"
    source = "EURO_NCAP_2023"
    source_file = "https://cdn.euroncap.com/media/77302/euro-ncap-aeb-c2c-test-protocol-v42.pdf"
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', 'close proximity', "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite']
    }
    #####   guest actor  #####
    guest_actor_type = ["vehicle"]
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": []
    }


@dataclass
class Car2PedFrontHeadon(Car2CarFrontHeadon):
    SC_ID = "SC_10"
    description = "Car-to-pedestrian_front_headon"
    guest_actor_type = ["pedestrian"]


@dataclass
class Car2CycFrontHeadon(Car2CarFrontHeadon):
    SC_ID = "SC_4"
    description = "Car-to-cyclist_front_headon"
    guest_actor_type = ["cyclist"]


@dataclass
class Car2CarCrossStraight(SCBasis):
    #####   general info    #####
    SC_ID = "SC2"
    description = "Car-to-car_crossing_straight_crossing_path"
    source = "EURO_NCAP_2023"
    source_file = "https://cdn.euroncap.com/media/77302/euro-ncap-aeb-c2c-test-protocol-v42.pdf"
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision', 'close proximity', "estimated collision+close proximity"],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['left', 'right']
    }
    #####   guest actor  #####
    guest_actor_type = ["vehicle"]
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        # "lo_act": ['accelerating', 'cruising', 'decelerating', 'standing still'],
        "la_act": ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": []
    }


@dataclass
class Car2PedCrossStraight(Car2CarCrossStraight):
    SC_ID = "SC_7"
    description = "Car-to-pedestrian_crossing_straight_crossing_path"
    guest_actor_type = ["pedestrian"]


@dataclass
class Car2CycCrossStraight(Car2CarCrossStraight):
    SC_ID = "SC_12"
    description = "Car-to-cyclist_crossing_straight_crossing_path"
    guest_actor_type = ["cyclist"]


@dataclass
class CarViolateTrafficLight(SCBasis):
    #####   general info    #####
    SC_ID = "SC11"
    description = "Car violates traffic light"
    source = ""
    source_file = ""
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": [],
        'la_act': [],
        "road_relation": ['staying', 'entering', 'leaving'],
        "road_type": ['controlled_lane'],
        "inter_actor_relation": [],
        "inter_actor_position": []
    }
    #####   guest actor  #####
    # skip
    #####    environment  #####
    envr_tag = {
        'light_state': ['Arrow stop', 'Stop', 'Flashing stop']
    }


@dataclass
class Car2CycPassingby(SCBasis):
    #####   general info    #####
    SC_ID = "SC_13"
    description = "The car and the bicyclist are going straight with a close proximity. The cyclist is on the left or right side to the car."
    source = ""
    source_file = ""
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating', 'standing still'],  # forward
        'la_act': ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['close proximity', "estimated collision+close proximity"],
        "inter_actor_position": ['left', 'right'],
        'inter_actor_heading': ['same']
    }
    #####   guest actor  #####
    guest_actor_type = ["cyclist"]
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating', 'standing still'],
        "la_act": ['swerving left', 'swerving right', 'going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": []
    }


@dataclass
class Car2CarFrontTurnRight(Car2CarFrontTurnLeft):
    #####   general info    #####
    SC_ID = "SC14"

    #####   host actor  #####
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning right'],
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', "close proximity", "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite']
    }


class Car2PedFrontTurnRight(Car2PedFrontTurnLeft):
    #####   general info    #####
    SC_ID = "SC15"

    #####   host actor  #####
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning right'],
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', "close proximity", "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite']
    }


class Car2CycFrontTurnRight(Car2CycFrontTurnLeft):
    #####   general info    #####
    SC_ID = "SC16"

    #####   host actor  #####
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning right'],
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', "close proximity", "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite']
    }




@dataclass
class Car2PedReverseMoving(SCBasis):
    #####   general info    #####
    SC_ID = "SC17"
    description = "Car-to-ped_reverse_moving"
    source = "EURO_NCAP_2023"
    source_file = "https://cdn.euroncap.com/media/77299/euro-ncap-aeb-lss-vru-test-protocol-v44.pdf"
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['reversing'],
        'la_act': ['swerving left', 'turning left', 'going straight', 'turning right', 'swerving right'],  # any
        "road_relation": [],
        "road_type": [],
        # "inter_actor_relation": ['estimated collision', "close proximity", "estimated collision+close proximity"],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['back'],
        'inter_actor_heading': ['not related', 'same', 'left', 'right', 'opposite', 'unknown']  # any
    }

    #####   guest actor  #####
    guest_actor_type = ["pedestrian"]
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating', 'reversing'],  # moving
        "la_act": ['swerving left', 'turning left', 'going straight', 'turning right', 'swerving right'],  # any
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': []
    }

@dataclass
class Car2PedReverseStationary(Car2PedReverseMoving):
    #####   general info    #####
    SC_ID = "SC18"

    #####   guest actor  #####
    guest_actor_tag = {
        "lo_act": ['standing still'],  # stationary
        "la_act": ['swerving left', 'turning left', 'going straight', 'turning right', 'swerving right'],  # any
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': []
    }




@dataclass
class CarTurnsLeft(SCBasis):
    #####   general info    #####
    SC_ID = "SC19"
    description = ""
    source = ""
    source_file = ""
    #####   host actor  #####
    host_actor_type = ["vehicle"]
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': []
    }
    #####   guest actor  #####
    # skip


@dataclass
class CarTurnsRight(CarTurnsLeft):
    #####   general info    #####
    SC_ID = "SC20"
    #####   host actor  #####
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],  # forward
        'la_act': ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': []
    }

@dataclass
class CycTurnsLeft(CarTurnsLeft):
    #####   general info    #####
    SC_ID = "SC21"
    host_actor_type = ["cyclist"]

@dataclass
class CycTurnsRight(CarTurnsRight):
    #####   general info    #####
    SC_ID = "SC22"
    host_actor_type = ["cyclist"]














scenario_catalog = {
    "SC1": Car2CarFrontTurnLeft,
    "SC8": Car2PedFrontTurnLeft,
    "SC5": Car2CycFrontTurnLeft,

    "SC14": Car2CarFrontTurnRight,
    "SC15": Car2PedFrontTurnRight,
    "SC16": Car2CycFrontTurnRight,

    "SC3": Car2CarFrontHeadon,
    # "SC10": Car2PedFrontHeadon,
    # "SC4": Car2CycFrontHeadon,

    "SC11": CarViolateTrafficLight,

    "SC2": Car2CarCrossStraight,
    "SC7": Car2PedCrossStraight,

    "SC13": Car2CycPassingby,
    "SC19": CarTurnsLeft,
    "SC20": CarTurnsRight,
    "SC21": CycTurnsLeft,
    "SC22": CycTurnsRight,


}