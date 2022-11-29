import random

env = simpy.Environment()

NUM_MOUSE = 100
NUM_FOOD = 100
NUM_FOODMOVEDBYB = 2
WATER_PENALTY = 1
FOOD_REQUIRED_PER_MOUSE = 1 # borderline food requirement to reward behavior. food intake above this number will be rewarded.
BEHAVIOR_REWARD_STRENGTH = 1 # 1 is default. constant multiplied to how much a 
SIMULATION_TIME = 30
BEHAVIOR_DIC = {"A":"hunt","B":"scavenge","C":"stayhome"}

class Mouse:
    def __init__(self, behavior_dic):
        self.env = env
        self.preference = {x:100/len(behavior_dic) for x in behavior_dic} # initial percentage of mouse taking an action
    
    def decide_behavior(self):
        randnum = random.uniform(0,100)
        behav_border_dic = {}
        for i,x in enumerate(self.preference):
            _bordervalue = sum([list(self.preference.values())[idx] for idx in range(i+1)])
            behav_border_dic[x] = _bordervalue

        preference_range = {x:x}
        self.behavior = sdf
        
    def update_preference(self):
        pass

def create_mouse_list(num_mouse):
    """make n mice for simulation"""
    mouse_list = [Mouse() for i in range(num_mouse)]
    return mouse_list

def simulation_process():

    for mouse in mouse_list:
        mouse.decide_behavior()
    yield env.timeout(1)


if __name__ == "__main__":
    cerberus = Mouse()