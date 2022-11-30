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
        df = df.groupby('Behavior Taken', sort=True).count().rename(columns={"Behavior Preference":idx+1})[idx+1]
        temp_list.append(df)
    
    return pd.concat(temp_list,axis=1)

def visualize_stackplot(df, title="Behavior Count", supplementary_text=""):
    """draw stackplot with matplotlib"""
    # draw stackplot
    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot()
    
    ax.text(80,103,supplementary_text, fontsize=8)
    plt.stackplot(df.columns, df)
    plt.legend(df.index, loc='upper left')
    plt.margins(0,0)
    plt.suptitle(title, fontsize=15)
    plt.xlabel("# of cycles", fontsize=12)
    plt.ylabel("# of mice", fontsize=12)
    plt.show()


if __name__ == "__main__":
    # run simulation
    data_list = sim.run_full_simulation()

    df_list = create_df_list(data_list)
    df_behaviorcount = create_behaviorcount_per_cycle(df_list)
    visualize_stackplot(df_behaviorcount, supplementary_text=f"Food : {sim.NUM_FOOD} \nSwimPen : -{sim.WATER_PENALTY} \nCarryCap : {sim.NUM_FOOD_MOVEDBY_MOUSE}")