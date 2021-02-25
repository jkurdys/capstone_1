# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def make_hist(df, f_name, title, xlabel, ylabel, save=True,):
    plt.figure(figsize=(12,6))
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.hist(df, bins=80)
    
    if save:
        plt.savefig(f'../images/{f_name}.png')
        return print('image saved')
    else:
        return plt.show()
       

if __name__ == '__main__':

    oct_all = pd.read_csv('tbl_prod_GABU202010_all.csv', sep= '|')
    oct_adds = pd.read_csv('tbl_prod_GABU202010_new_records.csv', sep= '|')
    oct_drops = pd.read_csv('tbl_prod_GABU202010_dropped_records.csv', sep= '|')

# calculate some state-level registration totals
    oct_state_tot = oct_all['registration_number'].count()
    oct_state_adds = oct_adds['registration_number'].count()
    oct_state_drops = oct_drops['registration_number'].count()

# calculate some state-level mean values
    oct_mean_adds_state = oct_state_adds / oct_state_tot
    oct_mean_drops_state = oct_state_drops / oct_state_tot

# calculate some geographic totals and mean values
    oct_county_tots = oct_all.groupby('county_code').count()['registration_number']
    oct_county_adds = oct_adds.groupby('county_code').count()['registration_number']

    oct_county_mean_adds = oct_county_adds / oct_county_tots
    
    make_hist(oct_county_tots, f_name='oct_county_tots', title='Distribution of Georgia Counties by Total Registered Voters', xlabel='Population of Registered Voters', ylabel='Number of Counties')
    