import random

NUM_MOUSE = 100
NUM_FOOD = 100
NUM_FOOD_MOVEDBY_MOUSE = 2
WATER_PENALTY = 0.8
REQUIRED_FOOD_PER_MOUSE = 1 # borderline food requirement to reward behavior. food intake above this number will be rewarded.
BEHAVIOR_REWARD_STRENGTH = 1 # constant multiplied to how much a mouse is rewarded/punished
SIMULATION_TIME = 400 # repeat simulation this amount of times
BEHAVIOR_NAME_DIC = {"A":"hunt","B":"scavenge","C":"stayhome"}
# INITIAL_BEHAVIOR_PREFERENCE = {bh_code:100/len(BEHAVIOR_NAME_DIC) for bh_code in BEHAVIOR_NAME_DIC}
# INITIAL_BEHAVIOR_PREFERENCE = {"A":33,"B":33,"C":34}
### bug when providing value as instance for class constructor... but why..? ###
MINIMUM_PROBABILITY = 1 # behavior occurance probability will not go lower than this %


class Mouse:
    def __init__(self, mouse_name, behavior_name_dic):
        self.name = mouse_name
        self.behavior_name_dic = behavior_name_dic
        # self.preference = {bh_code:100/len(BEHAVIOR_NAME_DIC) for bh_code in BEHAVIOR_NAME_DIC} # initial probability(%) of mouse selecting a behavior
        self.preference = {"A":1,"B":1,"C":98}
        self.position = "pf_home"
    
    def decide_behavior(self):
        """randomly pick a behavior according to self.preference"""
        randnum = random.uniform(0,100)
        for i,bh_code in enumerate(self.preference):
            bordervalue = sum([list(self.preference.values())[idx] for idx in range(i+1)])
            if randnum < bordervalue:
                self.behavior = bh_code #behavior returned as bh_code of behavior_name_dic argument
                break
    
    # behaviors
    def behave(self, num_food_movedby_mouse, water_penalty=WATER_PENALTY):
        """act upon self.behavior and change the environment"""
        global Environment
        # hunt
        if self.behavior == "A":
            Environment["pf_home"]["num_mouse"] -=1
            Environment["pf_food"]["num_mouse"] +=1
            self.position = "pf_food"
            self.water_penalty = water_penalty
        elif self.behavior == "B":
            if Environment["pf_food"]["num_food"] != 0:
                Environment["pf_food"]["num_food"] -= num_food_movedby_mouse
                Environment["pf_home"]["num_food"] += num_food_movedby_mouse
                if Environment["pf_food"]["num_food"] < 0:
                    Environment["pf_home"]["num_food"] += Environment["pf_food"]["num_food"]
                    Environment["pf_food"]["num_food"] = 0
            self.water_penalty = water_penalty
        elif self.behavior == "C":
            self.water_penalty = 0
            pass
    
    def calculate_food_acquired(self):
        global Environment
        self.food_acquired = Environment[self.position]["num_food"] / Environment[self.position]["num_mouse"] - self.water_penalty
        # <<sidenote>> will denominator always be bigger than 0?

    def update_preference(self, required_food_per_mouse, behavior_reward_strength, minimum_probability):
        """update preference according to self.food_acquired"""

        # increase/decrease all probabilities according to food_acquired.
        for bh_code in self.preference:
            if bh_code == self.behavior:
                self.preference[bh_code] += behavior_reward_strength * (len(self.preference)-1) * (self.food_acquired - required_food_per_mouse)
            else:
                self.preference[bh_code] += behavior_reward_strength * (required_food_per_mouse - self.food_acquired)

        # prevent any probability from going below minimum_probability. if so, take from other probabilities to raise to 1%.
        for bh_code,value in self.preference.items():
            if value < minimum_probability:
                # subtract percentage from max preference, repeated getting max _ times to distribute amount if max preference is similar.
                for _ in range(len(self.preference)-1):
                    self.preference[max(self.preference, key=self.preference.get)] -= (minimum_probability - value) / (len(self.preference)-1)
                self.preference[bh_code] = minimum_probability
    
    def get_behavior_name(self):
        return self.behavior_name_dic[self.behavior]
    
    def get_preference(self):
        return {self.behavior_name_dic[bh_code]:self.preference[bh_code] for bh_code in self.behavior_name_dic}

    def go_home(self):
        """reset mouse position to home"""
        self.position = "pf_home"


def create_mouse_list(num_mouse=NUM_MOUSE):
    """initialize n mouse objects for simulation. input number of mice, return mouse_list"""
    mouse_list = [Mouse(mouse_name= "mouse" + str(i+1), behavior_name_dic= BEHAVIOR_NAME_DIC) for i in range(num_mouse)]
    return mouse_list

def get_data(mouse_list):
    """get 2d list of current mouse status for all mice in mouse_list."""
    data = [[mouse.name, mouse.get_preference(), mouse.get_behavior_name(), mouse.food_acquired] for mouse in mouse_list]
    return data

def run_simulation(mouse_list, num_food_movedby_mouse=NUM_FOOD_MOVEDBY_MOUSE, required_food_per_mouse=REQUIRED_FOOD_PER_MOUSE, behavior_reward_strength=BEHAVIOR_REWARD_STRENGTH, minimum_probability=MINIMUM_PROBABILITY):
    """run one cycle of the full simulation ."""
    global Environment

    # update environment according to each mouse behavior
    for mouse in mouse_list:
        mouse.decide_behavior()
        mouse.behave(num_food_movedby_mouse)

    # update each mouse preference according to environment
    for mouse in mouse_list:
        mouse.calculate_food_acquired()
        mouse.update_preference(required_food_per_mouse, behavior_reward_strength, minimum_probability)
        mouse.go_home()
    
    return mouse_list

def set_environment(num_mouse=NUM_MOUSE, num_food=NUM_FOOD):
    """may use to reset environment in other files"""
    global Environment
    Environment = {"pf_home":{"num_mouse":num_mouse,"num_food":0},"pf_food":{"num_mouse":0,"num_food":num_food}}

def run_full_simulation(simulation_time=SIMULATION_TIME):
    """function for convenience. will run simulation for intended amount of times. returns 3d data list"""
    # initialize data list
    data_list = []

    # initialize objects
    mouse_list = create_mouse_list()

    # run simulation
    for _ in range(simulation_time):
        # reset environment status
        set_environment()

        mouse_list = run_simulation(mouse_list)
        data_list.append(get_data(mouse_list))

    return data_list


if __name__ == "__main__":
    pass
