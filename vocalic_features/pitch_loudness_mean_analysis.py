

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load eGeMAPSv02 result file
result_data = pd.read_csv('raw_features.csv')
playerList = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo']
deceiversList = ['Alpha', 'Delta']


# Replace the period with an underscore in column name
original_column_name = result_data.columns.tolist()
new_column_name = [col.replace('.', '_') for col in original_column_name]
new_column_name = [col.replace('-', '_') for col in new_column_name]

# Update the column names
result_data.columns = new_column_name

# Search for columns containing "mean" or "amean"
pitch_mean_columns = [col for col in result_data.columns if 'mean' in col and 'semitone' in col]

loudness_mean_columns = [col for col in result_data.columns if 'mean' in col and 'loudness' in col]

result_data = result_data[result_data['game'].str.contains('Speaker')]
#remove XC422A Bravo
remove = result_data['game'].str.contains('XC422A') & result_data['game'].str.contains('Bravo')
result_data = result_data[~remove]


# game info
result_data['game'] = result_data['game'].str.replace('_Speaker.mp3', '')

# split the 'game' column into multiple columns
result_data[['game', 'stage', 'speaker']] = result_data['game'].str.split('_', expand=True)

# count the number of occurrences of each group
result_data.groupby(['game', 'stage']).size()

# create a dictionary to map player to roles
def categorize_player(player):
    if player in deceiversList:
        return 'Deceiver'
    else:
        return 'Truth_teller'


# create a new 'role' column based on the 'player' column
result_data['role'] = result_data['speaker'].map(categorize_player)
result_data.info()

def run_anova(variable_List):
    for variable in variable_List:
        formula = f'{variable} ~ role'
        print(formula)
        model = ols(formula, data=result_data).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        print(anova_table)

        formula = f'{variable} ~ role*stage'
        print(formula)
        model = ols(formula, data=result_data).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        print(anova_table)


run_anova(pitch_mean_columns)
run_anova(loudness_mean_columns)

model = ols('F0semitoneFrom27_5Hz_sma3nz_amean ~ role', data=result_data).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# create a boxplot to compare the distribution of the two groups

sns.boxplot(x='role', y='F0semitoneFrom27_5Hz_sma3nz_stddevNorm', hue='stage', data=result_data)

sns.boxplot(x='role', y='loudness_sma3_amean', hue='stage', data=result_data)

def run_anova_all(variable_List):
    variable_List = new_column_name[:-1]
    for variable in variable_List:
        print(variable)

        formula = f'{variable} ~ role'
        model1 = ols(formula, data=result_data).fit()

        # Perform ANOVA and filter p-values less than 0.05
        pvalues = model1.pvalues[model1.pvalues.index[1]]
        if pvalues < 0.05:
            print(formula)
            anova_table1 = sm.stats.anova_lm(model1, typ=2)
            print(anova_table1)

        formula = f'{variable} ~ role*stage'
        model2 = ols(formula, data=result_data).fit()

        # Perform ANOVA and filter interaction p-values less than 0.05
        interaction_pvalues = model2.pvalues[model2.pvalues.index.str.contains(':')]
        significant_interactions = interaction_pvalues[interaction_pvalues < 0.05]
        if significant_interactions.any():
            print(formula)
            anova_table2 = sm.stats.anova_lm(model2, typ=2)
            print(anova_table2)

run_anova_all(new_column_name[1])
