import pandas as pd
from scipy import stats

# Load the group feature and original data into a DataFrame
pc_group = pd.read_csv('grouped_vars_varimax.csv')
df_original = pd.read_csv('raw_features.csv')
# Extract the feature columns, remove discussion section
df_original = df_original[df_original['game'].str.contains('Speaker')]
#remove XC422A Bravo
remove = df_original['game'].str.contains('XC422A') & df_original['game'].str.contains('Bravo')
df_original = df_original[~remove]

# change the name of index to column with name 'Feature'
pc_group.rename(columns={'Unnamed: 0': 'feature'}, inplace=True)
pc_group.columns

def cronbach_alpha(data):
    # Transform the data frame into a correlation matrix
    df_corr = data.corr()

    # Calculate N
    # The number of variables is equal to the number of columns in the dataframe
    N = data.shape[1]

    # Calculate r
    # For this, we'll loop through all the columns and append every
    # relevant correlation to an array called 'r_s'. Then, we'll
    # calculate the mean of 'r_s'.
    rs = np.array([])
    for i, col in enumerate(df_corr.columns):
        sum_ = df_corr[col][i + 1:].values
        rs = np.append(sum_, rs)
    mean_r = np.mean(rs)

    # Use the formula to calculate Cronbach's Alpha
    cronbach_alpha = (N * mean_r) / (1 + (N - 1) * mean_r)
    return cronbach_alpha

# for PC each group
for group_num in set(pc_group['PC']):
    print(group_num)
    cal = pd.DataFrame()
    # find features under the same PC group
    for feature_loads in pc_group[pc_group['PC'] == group_num].values:
        col_name = feature_loads[0]
        load_var = feature_loads[2]

        print(feature_loads)
        if load_var < 0:  # if load is negative
            # Include the negative value of the column
            cal[col_name] = -df_original[col_name]
        else:
            # Include the original value of the column
            cal[col_name] = df_original[col_name]

    # calculate Cronbach's alpha for each factor
    print("Factor", group_num, "Cronbach's alpha:", cronbach_alpha(cal))

    # average of each PC
    row_means = cal.mean(axis=1)
    df_original[group_num] = row_means


grouped = df_original.iloc[:, -7:]
grouped.columns
# change the column name from 'A' to 'X'
grouped = grouped.rename(columns={'PC1': 'amplitude', 'PC2': 'pitch', 'PC3': 'loudness', 'PC4': 'spectral_high_freq',
                                  'PC5': 'spectral_variance', 'PC6': 'vowel'})

grouped.to_csv('vocal_grouped.csv', index=True)

