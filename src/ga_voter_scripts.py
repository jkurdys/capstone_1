'''
This script is currently configured to save plotted images in an adjacent /images
directory and print the p-values for tests of various geographic, demographic and
partisan subsets of the population.

This script must be run in the same directory as the user's dataset. For more 
information on the dataset and how to download it, consult the README.
'''

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#if __name__ == '__main__':
# these variables need to be indented under the if __name__ block

# read in csvs
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

# oct_county_tots.hist(bins=159, figsize=(12,6))
# oct_county_adds.hist(bins=159, figsize=(12,6))

# calculate some demographic totals and mean values
oct_gender_tots = oct_all.groupby('gender').count()['registration_number']
oct_gender_adds = oct_adds.groupby('gender').count()['registration_number']

oct_gender_mean_adds = oct_gender_adds / oct_gender_tots

# calculate partisan totals and mean values
oct_party_tots = oct_all.groupby('party_last_voted').count()['registration_number']
oct_party_adds = oct_adds.groupby('party_last_voted').count()['registration_number']
oct_party_drops = oct_drops.groupby('party_last_voted').count()['registration_number']

oct_party_mean_adds = oct_party_adds / oct_party_tots
oct_party_mean_drops = oct_party_drops / oct_party_tots

# geographic statistical tests and plots

ot5 = oct_county_mean_adds.sort_values(ascending=False)

plt.figure(figsize=(12,6))
x = ot5

plt.title("Distribution of New Voter Registration Rates by County")
plt.xlabel("County-level New Voter Registration Rate (percent)")
plt.ylabel("Number of Counties")

plt.hist(x * 100, bins=80)
plt.savefig('../images/county_rates_hist.png')
# plt.show()

plt.figure(figsize=(12,6))
x = np.array(["91", "127", "57", "89", "21", "SM", "CM"])
y = np.array([0.048399, 0.038796, 0.036528, 0.036430, 0.035231, 0.02124921711756242, 0.02073116526145582])

plt.title("Top 5 New Voter Registration Rates by County")
plt.xlabel("County Code, State Mean, County-level Mean")
plt.ylabel("Mean Rate of New Registrations")

plt.bar(x,y)
plt.savefig('../images/top5_bar.png')
# plt.show()

# registrations by county
county91_tot_regs = oct_all[oct_all['county_code'] == 91]
county127_tot_regs = oct_all[oct_all['county_code'] == 127]
county57_tot_regs = oct_all[oct_all['county_code'] == 57]
county89_tot_regs = oct_all[oct_all['county_code'] == 89]
county21_tot_regs = oct_all[oct_all['county_code'] == 21]

# new registrations by county
county91_regs = oct_adds[oct_adds['county_code'] == 91]
county127_regs = oct_adds[oct_adds['county_code'] == 127]
county57_regs = oct_adds[oct_adds['county_code'] == 57]
county89_regs = oct_adds[oct_adds['county_code'] == 89]
county21_regs = oct_adds[oct_adds['county_code'] == 21]

# total registered voters by county
county91_oct_tot = county91_tot_regs['registration_number'].count()
county127_oct_tot = county127_tot_regs['registration_number'].count()
county57_oct_tot = county57_tot_regs['registration_number'].count()
county89_oct_tot = county89_tot_regs['registration_number'].count()
county21_oct_tot = county21_tot_regs['registration_number'].count()

# newly registered voters by county
county91_oct_adds = county91_regs['registration_number'].count()
county127_oct_adds = county127_regs['registration_number'].count()
county57_oct_adds = county57_regs['registration_number'].count()
county89_oct_adds = county89_regs['registration_number'].count()
county21_oct_adds = county21_regs['registration_number'].count()

# making county-level binomial distributions
county91_binomial = stats.binom(n=county91_oct_tot, p=oct_county_mean_adds.mean())
county127_binomial = stats.binom(n=county127_oct_tot, p=oct_county_mean_adds.mean())
county57_binomial = stats.binom(n=county57_oct_tot, p=oct_county_mean_adds.mean())
county89_binomial = stats.binom(n=county89_oct_tot, p=oct_county_mean_adds.mean())
county21_binomial = stats.binom(n=county21_oct_tot, p=oct_county_mean_adds.mean())

# calculating county-specific p-values
county91_cdf = 1 - county91_binomial.cdf(county91_oct_adds)
county127_cdf = 1 - county127_binomial.cdf(county127_oct_adds)
county57_cdf = 1 - county57_binomial.cdf(county57_oct_adds)
county89_cdf = 1 - county89_binomial.cdf(county89_oct_adds)
county21_cdf = 1 - county21_binomial.cdf(county21_oct_adds)

# we see nothing below a 0.05 rejection threshhold to warrant rejecting the null hypothesis
print(f"p-values for CDF of geographic binomial distribution using normalized county mean:\n County code 91: {county91_cdf}\n County code 127: {county127_cdf}\n County code 57: {county57_cdf}\n County code 89: {county89_cdf}\n County code 21: {county21_cdf}")

# demographic statistical tests and plots
# registrations by gender 
f_tot_regs = oct_all[oct_all['gender'] == 'F']
m_tot_regs = oct_all[oct_all['gender'] == 'M']
o_tot_regs = oct_all[oct_all['gender'] == 'O']

# new registrations by gender
f_regs = oct_adds[oct_adds['gender'] == 'F']
m_regs = oct_adds[oct_adds['gender'] == 'M']
o_regs = oct_adds[oct_adds['gender'] == 'O']

# total registered voters by gender
f_oct_tot = f_tot_regs['registration_number'].count()
m_oct_tot = m_tot_regs['registration_number'].count()
o_oct_tot = o_tot_regs['registration_number'].count()

# newly registered voters by gender
f_oct_adds = f_regs['registration_number'].count()
m_oct_adds = m_regs['registration_number'].count()
o_oct_adds = o_regs['registration_number'].count()

plt.figure(figsize=(12,6))
x = np.array(["O","GM", "M", "SM", "F"])
y = np.array([oct_gender_mean_adds[2], oct_gender_mean_adds.mean(), oct_gender_mean_adds[1], oct_mean_adds_state, oct_gender_mean_adds[0]])

plt.title("New Voter Registration Rates by Gender")
plt.xlabel("Gender Code, State Mean, Gender Mean (sorted)")
plt.ylabel("Mean Rate of New Registrations")

plt.bar(x,y)
plt.savefig('../images/gender_rates_bar.png')
# plt.show()

# binomials based on gender mean
fgm_binomial = stats.binom(n=f_oct_tot, p=oct_gender_mean_adds.mean())
mgm_binomial = stats.binom(n=m_oct_tot, p=oct_gender_mean_adds.mean())
ogm_binomial = stats.binom(n=o_oct_tot, p=oct_gender_mean_adds.mean())

# binomials based on state mean
fsm_binomial = stats.binom(n=f_oct_tot, p=oct_mean_adds_state)
msm_binomial = stats.binom(n=m_oct_tot, p=oct_mean_adds_state)
osm_binomial = stats.binom(n=o_oct_tot, p=oct_mean_adds_state)

# calculating p-values based on gender mean
fgm_cdf = 1 - fgm_binomial.cdf(f_oct_adds)
mgm_cdf = 1 - mgm_binomial.cdf(m_oct_adds)
ogm_cdf = 1 - ogm_binomial.cdf(o_oct_adds)

# calculating p-values based on state mean
fsm_cdf = 1 - fsm_binomial.cdf(f_oct_adds)
msm_cdf = 1 - msm_binomial.cdf(m_oct_adds)
osm_cdf = 1 - osm_binomial.cdf(o_oct_adds)

# we see nothing below a 0.05 rejection threshhold to warrant rejecting the null hypothesis
# using the gender mean.
print(f"p-values for CDF of demographic binomial distribution using normalized gender mean:\n Female: {fgm_cdf}\n Male: {mgm_cdf}\n Other: {ogm_cdf}")

# we see nothing below a 0.05 rejection threshhold to warrant rejecting the null hypothesis
# using the state mean.
print(f"p-values for CDF of demographic binomial distribution using simple state mean:\n Female: {fsm_cdf}\n Male: {msm_cdf}\n Other: {osm_cdf}")

# partisan statistical tests and plots
plt.figure(figsize=(5,5))
x = np.array(["State adds", "State drops"])
y = np.array([oct_state_adds, oct_state_drops])

plt.title("October 2020 Statewide Added/Dropped Registrations")
plt.xlabel("Statewide Adds/Drops")
plt.ylabel("Number of Added/Dropped Registrations")

plt.bar(x,y)
plt.savefig('../images/state_add_drop_bar.png')
# plt.show()

plt.figure(figsize=(12,6))
x = np.array(["D", "N", "NP", "R"])
y = np.array([oct_party_tots[0],  oct_party_tots[1], oct_party_tots[2], oct_party_tots[3]])

plt.title("October 2020 Total Registrations by Party")
plt.xlabel("Party")
plt.ylabel("Total Registrations")

plt.bar(x,y)
plt.savefig('../images/party_registrations_bar.png')
# plt.show()

plt.figure(figsize=(12,6))
x = np.array(["D adds", "D drops", "N adds", "N drops", "NP adds", "NP drops", "R adds", "R drops"])
y = np.array([oct_party_adds[0], oct_party_drops[0],oct_party_adds[1], oct_party_drops[1],oct_party_adds[2], oct_party_drops[2],oct_party_adds[3], oct_party_drops[3]])

plt.title("October 2020 Added/Dropped Registrations by Party")
plt.xlabel("Party Adds/Drops")
plt.ylabel("Number of Added/Dropped Registrations")

plt.bar(x,y)
plt.savefig('../images/party_add_drops_bar.png')
# plt.show()

# registrations by party (D, N, NP, R)
d_tot_regs = oct_all[oct_all['party_last_voted'] == 'D']
n_tot_regs = oct_all[oct_all['party_last_voted'] == 'N']
np_tot_regs = oct_all[oct_all['party_last_voted'] == 'NP']
r_tot_regs = oct_all[oct_all['party_last_voted'] == 'R']

# new registrations by party
d_regs = oct_adds[oct_adds['party_last_voted'] == 'D']
n_regs = oct_adds[oct_adds['party_last_voted'] == 'N']
np_regs = oct_adds[oct_adds['party_last_voted'] == 'NP']
r_regs = oct_adds[oct_adds['party_last_voted'] == 'R']

# total registered voters by party
d_oct_tot = d_tot_regs['registration_number'].count()
n_oct_tot = n_tot_regs['registration_number'].count()
np_oct_tot = np_tot_regs['registration_number'].count()
r_oct_tot = r_tot_regs['registration_number'].count()

# newly registered voters by party
d_oct_drops = d_regs['registration_number'].count()
n_oct_drops = n_regs['registration_number'].count()
np_oct_drops = np_regs['registration_number'].count()
r_oct_drops = r_regs['registration_number'].count()

# binomials based on party mean
dpm_binomial = stats.binom(n=d_oct_tot, p=oct_party_mean_drops.mean())
npm_binomial = stats.binom(n=n_oct_tot, p=oct_party_mean_drops.mean())
nppm_binomial = stats.binom(n=np_oct_tot, p=oct_party_mean_drops.mean())
rpm_binomial = stats.binom(n=r_oct_tot, p=oct_party_mean_drops.mean())

# binomials based on state mean
dsm_binomial = stats.binom(n=d_oct_tot, p=oct_mean_drops_state)
nsm_binomial = stats.binom(n=n_oct_tot, p=oct_mean_drops_state)
npsm_binomial = stats.binom(n=np_oct_tot, p=oct_mean_drops_state)
rsm_binomial = stats.binom(n=r_oct_tot, p=oct_mean_drops_state)

# calculating p-values based on party mean
dpm_cdf = 1 - dpm_binomial.cdf(d_oct_drops)
npm_cdf = 1 - npm_binomial.cdf(n_oct_drops)
nppm_cdf = 1 - nppm_binomial.cdf(np_oct_drops)
rpm_cdf = 1 - rpm_binomial.cdf(r_oct_drops)

# calculating p-values based on state mean
dsm_cdf = 1 - dsm_binomial.cdf(d_oct_drops)
nsm_cdf = 1 - nsm_binomial.cdf(n_oct_drops)
npsm_cdf = 1 - npsm_binomial.cdf(np_oct_drops)
rsm_cdf = 1 - rsm_binomial.cdf(r_oct_drops)

# we see nothing below a 0.05 rejection threshhold to warrant rejecting the null hypothesis
# using the party mean.
print(f"p-values for CDF of partisan binomial distribution using normalized party mean:\n Democrat: {dpm_cdf}\n Undeclared: {npm_cdf}\n Unaffiliated: {nppm_cdf}\n Republican: {rpm_cdf}")

# we see nothing below a 0.05 rejection threshhold to warrant rejecting the null hypothesis
# using the state mean.
print(f"p-values for CDF of partisan binomial distribution using simple state mean:\n Democrat: {dsm_cdf}\n Undeclared: {nsm_cdf}\n Unaffiliated: {npsm_cdf}\n Republican: {rsm_cdf}")