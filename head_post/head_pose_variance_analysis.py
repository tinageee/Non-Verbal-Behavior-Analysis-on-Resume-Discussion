import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

input_folder = '/Users/saiyingge/PycharmProjects/body/data/'
playerList = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo']
deceiversList = ['Alpha', 'Delta']
variable_List = ['pitch', 'roll', 'yaw']

# Read the three CSV files into separate dataframes
df1 = pd.read_csv(input_folder + 'pitch_all.csv')
df2 = pd.read_csv(input_folder + 'roll_all.csv')
df3 = pd.read_csv(input_folder + 'yaw_all.csv')

# Add a new column to each dataframe indicating the source file
df1 = df1.assign(head_p='pitch')
df2 = df2.assign(head_p='roll')
df3 = df3.assign(head_p='yaw')

# Concatenate the dataframes into a single dataframe
df = pd.concat([df1, df2, df3])

# Reset the index of the concatenated dataframe
df = df.reset_index(drop=True)

df.info()
df.describe()
df.columns

len(df)
df.isnull().sum()
df = df.dropna()
len(df)

variance_all = pd.DataFrame()
# Group the dataframe by the three columns of interest and calculate the variance of the "Value" column
for i in playerList:
    variances = df.groupby(['game', 'speaker', 'stage', 'head_p'])[i].var().reset_index()
    variances = variances.rename(columns={i: 'variance'})
    variances['player'] = i
    variance_all = pd.concat([variances, variance_all], axis=0)


##add deception

# create a dictionary to map player to roles
def categorize_player(player):
    if player in deceiversList:
        return 'deceiver'
    else:
        return 'Truth_teller'


# create a new 'role' column based on the 'player' column
variance_all['role'] = variance_all['player'].map(categorize_player)
variance_all.info()
variance_all.isnull().sum()
# variance_all['variance'] = pd.to_numeric(variance_all['variance'], errors='coerce')

# remove outliers
# Calculate the 95th percentile of the column
q95 = variance_all['variance'].quantile(0.95)

# Remove any values greater than the 95th percentile
variance_all = variance_all[variance_all['variance'] <= q95]

# anova test for all data
for x in variable_List:
    # fit an ANOVA model to the data
    model = ols('variance ~ role', data=variance_all[variance_all['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(x)
    print(anova_table)

    model = ols('variance ~ role*stage', data=variance_all[variance_all['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(anova_table)

# create a boxplot to compare the distribution of the two groups
sns.boxplot(x='head_p', y='variance', hue='stage', data=variance_all)
plt.legend(loc='upper center')
plt.title('head position variance among 3 stages')


# test for speaker in intro - note
variable_spk = variance_all.loc[variance_all['speaker'] == variance_all['player']]
for x in variable_List:
    # fit an ANOVA model to the data
    model = ols('variance ~ role', data=variable_spk[variable_spk['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(x)
    print(anova_table)

    model = ols('variance ~ role*stage', data=variable_spk[variable_spk['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(anova_table)

    # create a boxplot to compare the distribution of the two groups
sns.boxplot(x='stage', y='variance',  data=variable_spk[variable_spk['head_p'] == 'yaw'])
# add a title
plt.title('Speaker\'s Yaw')

# speaker is in the same group or not

def same_group(speaker, player):
    if (speaker in deceiversList and player in deceiversList) \
            or (speaker not in deceiversList and player not in deceiversList):
        return 'same'
    else:
        return 'diff'


variable_group = variance_all.loc[variance_all['speaker'] != variance_all['player']]
# Create a new column that indicates whether the speaker and player are in the same group
variable_group.loc[:, 'group'] = variable_group.apply(lambda row: same_group(row['speaker'], row['player']), axis=1)

for x in variable_List:
    # fit an ANOVA model to the data
    model = ols('variance ~ role', data=variable_group[variable_group['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(x)
    print(anova_table)

    model = ols('variance ~ role*group', data=variable_group[variable_group['head_p'] == x]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    # print the ANOVA table
    print(anova_table)


sns.boxplot(x='role', y='variance', hue='group', data=variable_group[variable_group['head_p'] == 'yaw'])
sns.boxplot(x='group', y='variance', data=variable_group[variable_group['head_p'] == 'yaw'])
plt.title('variance of yaw of listeners')

model = ols('variance ~ group', data=variable_group[variable_group['head_p'] == 'yaw']).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
# print the ANOVA table
print(anova_table)