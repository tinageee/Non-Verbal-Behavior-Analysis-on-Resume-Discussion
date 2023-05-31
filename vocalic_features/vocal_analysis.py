import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd


df = pd.read_csv('vocal_grouped.csv', index_col=None)
playerList = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo']
deceiversList = ['Alpha', 'Delta']
variable_List = ['amplitude', 'pitch', 'loudness', 'spectral_high_freq', 'spectral_variance', 'vowel']

df.info()
df.describe()
df.columns
df.isnull().sum()

# game info
df['game'] = df['game'].str.replace('_Speaker.mp3', '')

# split the 'game' column into multiple columns
df[['game', 'stage', 'speaker']] = df['game'].str.split('_', expand=True)

# count the number of occurrences of each group
df.groupby(['game', 'stage']).size()


# create a dictionary to map player to roles
def categorize_player(player):
    if player in deceiversList:
        return 'Deceiver'
    else:
        return 'Truth_teller'


# create a new 'role' column based on the 'player' column
df['role'] = df['speaker'].map(categorize_player)
df.info()

for variable in variable_List:
    formula = f'{variable} ~ role'
    print(formula)
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

    formula = f'{variable} ~ role*stage'
    print(formula)
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

# create a boxplot to compare the distribution of the two groups

sns.boxplot(x='role', y='spectral_variance', hue='stage', data=df)
plt.legend(loc='lower right')

print(pairwise_tukeyhsd(df["spectral_variance"], df["role"]))
print(pairwise_tukeyhsd(df["spectral_variance"], df["stage"]))
