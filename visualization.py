import pandas as pd
import matplotlib.pyplot as plt

import simulation as sim

COLUMN_NAMES = ["Mouse Name","Behavior Preference","Behavior Taken","Food Acquired"]


def create_df_list(list3d, column_names=COLUMN_NAMES):
    """get 3d list and make list of dataframes"""
    df_list = [pd.DataFrame(data, columns=column_names).set_index("Mouse Name") for data in list3d]
    return df_list

def create_behaviorcount_per_cycle(df_list):
    """return df_behaviorcount, has count of behaviors per each cycle"""
    temp_list = []
    for idx, df in enumerate(df_list):
        df = df.groupby('Behavior Taken', sort=False).count().rename(columns={"Behavior Preference":idx+1})[idx+1]
        temp_list.append(df)
    
    result = pd.concat(temp_list,axis=1).reindex(sim.BEHAVIOR_NAME_DIC.values())
    result = result.fillna(0)
    return result

def visualize_stackplot(df, title="Behavior Count", supplementary_text="", supp_text_2=""):
    """draw stackplot with matplotlib"""
    # draw stackplot
    plt.figure(figsize=(5,4))
    
    plt.text(len(df.columns),sim.NUM_MOUSE*51/50, supplementary_text, fontsize=8, ha="right")
    plt.text(0,sim.NUM_MOUSE*51/50, supp_text_2, fontsize=8, ha="left")
    plt.stackplot(df.columns, df)
    plt.legend(df.index, loc='upper left')
    plt.margins(0,0)
    plt.suptitle(title, fontsize=15)
    plt.xlabel("# of cycles", fontsize=12)
    plt.ylabel("# of mice", fontsize=12)
    plt.show()

### incomplete ###
def create_preference_df_list(list3d):
    """flatten preference dictionary"""
    pref_df_list = []
    for data in list3d:
        pref_ser_list = [pd.Series(mouse[1], name=mouse[0]) for mouse in data]
        df = pd.concat(pref_ser_list, axis=1)
        pref_df_list.append(df)

    return pref_df_list

def get_averagepreferencechange_per_cycle(pref_df_list):
    """get average change of all behavior preferences. returns df"""
    temp_list = []
    for dfidx,curr_df in enumerate(pref_df_list[:-1]):
        next_df = pref_df_list[dfidx+1]
        df = curr_df - next_df
        df_avgdelprep = pd.Series(df.sum(axis=1).divide(len(df.columns)), name=dfidx+1)
        temp_list.append(df_avgdelprep)

    delpref_df = pd.concat(temp_list, axis=1)
    return delpref_df

def visualize_preference_equilibrium(df):
    """to check for preference change equilibrium"""
    # draw lineplots
    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot()
    
    ax.text(80,103,supplementary_text, fontsize=8)
    
    plt.plot(x, y, label = "line 1")
    plt.plot(y, x, label = "line 2")
    plt.legend()
    plt.show()
### incomplete end ###

if __name__ == "__main__":
    # run simulation
    data_list = sim.run_full_simulation()

    df_list = create_df_list(data_list)
    df_behaviorcount = create_behaviorcount_per_cycle(df_list)
    visualize_stackplot(df_behaviorcount, 
        supp_text_2=f"Food : {sim.NUM_FOOD}\nSwimPen : -{sim.WATER_PENALTY}\nCarryCap : {sim.NUM_FOOD_MOVEDBY_MOUSE}",
        supplementary_text=f"RwrdStrgth : {sim.BEHAVIOR_REWARD_STRENGTH}\nFoodReq : {sim.REQUIRED_FOOD_PER_MOUSE}\nMinProb : {sim.MINIMUM_PROBABILITY}")


    # pref_df_list = create_preference_df_list(data_list)
    # print(create_preferencechange_per_cycle(pref_df_list))
