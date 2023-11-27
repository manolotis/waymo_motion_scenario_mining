
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

@dataclass
class SC1(SCBasis):
    #####   general info    #####
    SC_ID = "SC1"
    description = "Steering left"
    source = "CETRAN SC1 & SC2"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    Not distinguishing between turning and maneuvering a bend. Does not include swerving
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC2(SCBasis):
    #####   general info    #####
    SC_ID = "SC2"
    description = "Steering left"
    source = "CETRAN SC1 & SC3"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    Not distinguishing between turning and maneuvering a bend. Does not include swerving. Identical to SC1, but turning right
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC3(SCBasis):
    #####   general info    #####
    SC_ID = "SC3"
    description = "Driving straight"
    source = "CETRAN SC4"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -Cannot specify road_layout straight
-Scenario identified any timestep vehicle is going straight, so even if it turns briefly after that it would be identified as driving straight
-Would be fixed with road_layout tags, or supporting that other tags should not happen later (e.g. turning)
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC4(SCBasis):
    #####   general info    #####
    SC_ID = "SC4"
    description = "Vehicle backing up"
    source = "CETRAN SC16"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -Cannot support "same lane" definition yet.
-Cannot support "backing up into ego" yet. If we use "potential collision", ther would be a lot of false positives with other paked or stopped vehicles
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['reversing'],
        "la_act": ['swerving left', 'turning left', 'going straight', 'turning right', 'swerving right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC5(SCBasis):
    #####   general info    #####
    SC_ID = "SC5"
    description = "Oncoming vehicle"
    source = "CETRAN SC20"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -Cannot support "same lane" definition yet
-Likely resulting in a lot of FPs without the same lane tag
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC6(SCBasis):
    #####   general info    #####
    SC_ID = "SC6"
    description = "Ego vehicle approaching red traffic light"
    source = "CETRAN SC23"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for road layout specification
-No explicity support for approaching the traffic light itself, but can detect if vehicle staying/approaching or leaving controlled lane, and state of traffic line controlling this lane
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'approaching'],
        "road_type": ['controlled_lane'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC7(SCBasis):
    #####   general info    #####
    SC_ID = "SC7"
    description = "Ego vehicle approaching green traffic light"
    source = "CETRAN SC24"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for road layout specification
-No explicity support for approaching the traffic light itself, but can detect if vehicle staying/approaching or leaving controlled lane, and state of traffic line controlling this lane
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'approaching'],
        "road_type": ['controlled_lane'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC8(SCBasis):
    #####   general info    #####
    SC_ID = "SC8"
    description = "Ego vehicle approaching amber traffic light"
    source = "CETRAN SC25"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for road layout specification
-No explicity support for approaching the traffic light itself, but can detect if vehicle staying/approaching or leaving controlled lane, and state of traffic line controlling this lane
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'approaching'],
        "road_type": ['controlled_lane'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC9(SCBasis):
    #####   general info    #####
    SC_ID = "SC9"
    description = "Vehicle running red traffic light"
    source = "CETRAN SC26"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for road layout specification
-No explicity support for approaching the traffic light itself, but can detect if vehicle staying/approaching or leaving controlled lane, and state of traffic line controlling this lane
-Flashing red is not included since it's equivalent to stop sign
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['leaving'],
        "road_type": ['controlled_lane'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC10(SCBasis):
    #####   general info    #####
    SC_ID = "SC10"
    description = "Oncoming vehicle turns right at signalized junction"
    source = "CETRAN SC27"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction"
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC11(SCBasis):
    #####   general info    #####
    SC_ID = "SC11"
    description = "Ego vehicle turns right with oncoming vehicle at signalized junction"
    source = "CETRAN SC28"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction"
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC12(SCBasis):
    #####   general info    #####
    SC_ID = "SC12"
    description = "Oncoming vehicle turns right at non-signalized junction"
    source = "CETRAN SC29"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction", so it would be the same as SC10 (CETRAN SC27)
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC13(SCBasis):
    #####   general info    #####
    SC_ID = "SC13"
    description = "Oncoming vehicle turns right at non-signalized junction"
    source = "CETRAN SC30"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction", so it would be the same as SC11 (CETRAN SC28)
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC14(SCBasis):
    #####   general info    #####
    SC_ID = "SC14"
    description = "Ego straight with vehicle from left at non-signalized junction"
    source = "CETRAN SC31"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction"
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['left', 'front'],
        'inter_actor_heading': ['opposite', 'left'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight', 'turning left', 'turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC15(SCBasis):
    #####   general info    #####
    SC_ID = "SC15"
    description = "Vehicle straight with ego from left at non-signalized junction"
    source = "CETRAN SC32"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction"
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight', 'turning left', 'turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['right', 'front'],
        'inter_actor_heading': ['opposite', 'right'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC16(SCBasis):
    #####   general info    #####
    SC_ID = "SC16"
    description = "Undertaking at left turn at non-signalized junction"
    source = "CETRAN SC36"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specifying "signalized junction"
-No explicit support for undertaking. Would combine turning left + potential collision
-Probably quite a few FPs  when using "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision', 'close proximity'],
        "inter_actor_position": ['left'],
        'inter_actor_heading': ['same', 'left'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC17(SCBasis):
    #####   general info    #####
    SC_ID = "SC17"
    description = "Jaywalking"
    source = "CETRAN SC39"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No explicit support for specfying that pedestrian is not crossing at a zebra crossing
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['left', 'right'],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'leaving', 'approaching'],
        "road_type": ['freeway', 'surface_street', 'brokensinglewhite', 'brokensingleyellow', 'brokendoubleyellow', 'cross_walk'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC18(SCBasis):
    #####   general info    #####
    SC_ID = "SC18"
    description = "Pedestrian crossing at zebra crossing"
    source = "CETRAN SC40"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for specifying there are no traffic lights
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['left', 'right'],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'leaving', 'approaching'],
        "road_type": ['cross_walk'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC19(SCBasis):
    #####   general info    #####
    SC_ID = "SC19"
    description = "Zebra crossing"
    source = "CETRAN SC41"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for specifying there are no traffic lights
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": ['staying', 'entering', 'leaving', 'approaching'],
        "road_type": ['cross_walk'],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = []
    guest_actor_tag = {
        "lo_act": [],
        "la_act": [],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC20(SCBasis):
    #####   general info    #####
    SC_ID = "SC20"
    description = "Pedestrian at left turn at junction"
    source = "CETRAN SC46 SC47"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for (non)signalized junction. Would be same SC46 and SC47
-If vehicle and pedestrian opposite direction, likely many FPs for potential collisions
-To do propely, we need junction detection, so we can specify we only care if both Vehicle and ped. are on the same junction
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['left'],
        'inter_actor_heading': ['same', 'opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC21(SCBasis):
    #####   general info    #####
    SC_ID = "SC21"
    description = "Pedestrian at right turn at junction"
    source = "CETRAN SC49 SC50"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for (non)signalized junction. Would be same SC46 and SC47
-If vehicle and pedestrian opposite direction, likely many FPs for potential collisions
-To do propely, we need junction detection, so we can specify we only care if both Vehicle and ped. are on the same junction
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['left'],
        'inter_actor_heading': ['same', 'opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC22(SCBasis):
    #####   general info    #####
    SC_ID = "SC22"
    description = "Cyclist crossing from left side at junction"
    source = "CETRAN SC51 53"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for (non)signalized junction. Would be same as SC53
-Until we can detect junctions, will use "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['left', 'front'],
        'inter_actor_heading': ['right'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC23(SCBasis):
    #####   general info    #####
    SC_ID = "SC23"
    description = "Cyclist crossing from right side at junction"
    source = "CETRAN SC52 54"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for (non)signalized junction. Would be same as SC53
-Until we can detect junctions, will use "potential collision"
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['right', 'front'],
        'inter_actor_heading': ['left'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC24(SCBasis):
    #####   general info    #####
    SC_ID = "SC24"
    description = "Ego vehicle approaching cyclist riding in the same direction"
    source = "CETRAN SC55"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for "approaching" another actor
-No support for being on the same lane
-Definition would be practically identical to SC56, only with potential collision
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['same'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC25(SCBasis):
    #####   general info    #####
    SC_ID = "SC25"
    description = "Ego vehicle driving alongside a cyclist"
    source = "CETRAN SC56"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for "approaching" another actor
-No support for being on the same lane
-Definition would be practically identical to SC56, only with potential collision
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['close proximity'],
        "inter_actor_position": [],
        'inter_actor_heading': ['same'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC26(SCBasis):
    #####   general info    #####
    SC_ID = "SC26"
    description = "Ego vehicle approaching cyclist riding in opposite direction"
    source = "CETRAN SC57"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    -No support for "same lane". Replace by potential collision
-Likely yield many FPs
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC27(SCBasis):
    #####   general info    #####
    SC_ID = "SC27"
    description = "Cyclist at left turn at junction"
    source = "CETRAN SC58 SC59"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    Very similar to SC46 and SC 47, but with cyclist instead of pedestrian
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['left'],
        'inter_actor_heading': ['same', 'opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC28(SCBasis):
    #####   general info    #####
    SC_ID = "SC28"
    description = "Cyclist at right turn at junction"
    source = "CETRAN SC61 SC62"
    source_file = "VMAD-SG1-11-03 (NL) Scenario Categories_v1.7.pdf"
    notes = '''
    Very similar to SC46 and SC 47, but with cyclist instead of pedestrian
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['right'],
        'inter_actor_heading': ['same', 'opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['cyclist']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }



@dataclass
class SC29(SCBasis):
    #####   general info    #####
    SC_ID = "SC29"
    description = "Car to ped reverse moving"
    source = "EuroNCAP AEB VRU test protocol v44 - Sec. 7.2.6"
    source_file = "euro-ncap-aeb-lss-vru-test-protocol-v44.pdf"
    notes = '''
    -
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['reversing'],
        "la_act": ['going straight', 'turning left', 'turning right', 'swerving left', 'swerving right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision', 'close proximity'],
        "inter_actor_position": ['back'],
        'inter_actor_heading': [],
    }



@dataclass
class SC30(SCBasis):
    #####   general info    #####
    SC_ID = "SC30"
    description = "Car to ped reverse stationary"
    source = "EuroNCAP AEB VRU test protocol v44 - Sec. 7.2.6"
    source_file = "euro-ncap-aeb-lss-vru-test-protocol-v44.pdf"
    notes = '''
    -
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['reversing'],
        "la_act": ['going straight', 'turning left', 'turning right', 'swerving left', 'swerving right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }
    #####   guest actor  #####
    guest_actor_type = ['pedestrian']
    guest_actor_tag = {
        "lo_act": ['standing still'],
        "la_act": ['going straight', 'turning left', 'turning right', 'swerving left', 'swerving right'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision', 'close proximity'],
        "inter_actor_position": ['back'],
        'inter_actor_heading': [],
    }



@dataclass
class SC31(SCBasis):
    #####   general info    #####
    SC_ID = "SC31"
    description = "Car-to-Car Front Turn-Across-Path "
    source = "EuroNCAP AEB C2C Sec. 8.2.3"
    source_file = "euro-ncap-aeb-c2c-test-protocol-v42.pdf"
    notes = '''
    -
    '''
    #####   host actor  #####
    host_actor_type = ['vehicle']
    host_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['turning left'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": ['estimated collision'],
        "inter_actor_position": ['front'],
        'inter_actor_heading': ['opposite'],
    }
    #####   guest actor  #####
    guest_actor_type = ['vehicle']
    guest_actor_tag = {
        "lo_act": ['accelerating', 'cruising', 'decelerating'],
        "la_act": ['going straight'],
        "road_relation": [],
        "road_type": [],
        "inter_actor_relation": [],
        "inter_actor_position": [],
        'inter_actor_heading': [],
    }


scenario_catalog = {
    'SC1': SC1,
    'SC2': SC2,
    'SC3': SC3,
    'SC4': SC4,
    'SC5': SC5,
    'SC6': SC6,
    'SC7': SC7,
    'SC8': SC8,
    'SC9': SC9,
    'SC10': SC10,
    'SC11': SC11,
    'SC12': SC12,
    'SC13': SC13,
    'SC14': SC14,
    'SC15': SC15,
    'SC16': SC16,
    'SC17': SC17,
    'SC18': SC18,
    'SC19': SC19,
    'SC20': SC20,
    'SC21': SC21,
    'SC22': SC22,
    'SC23': SC23,
    'SC24': SC24,
    'SC25': SC25,
    'SC26': SC26,
    'SC27': SC27,
    'SC28': SC28,
    'SC29': SC29,
    'SC30': SC30,
    'SC31': SC31,
}
