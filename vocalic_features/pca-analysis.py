import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  # to standardize the features
from sklearn.decomposition import PCA  # to apply PCA
import seaborn as sns  # to plot the heat maps
from sklearn.decomposition import FactorAnalysis

# Load the eGeMAPSv02 feature data into a DataFrame
data = pd.read_csv('raw_features.csv')

#remove XC422A Bravo
data[data['game'].str.contains('XC422A') & data['game'].str.contains('Bravo')]
remove = data['game'].str.contains('XC422A') & data['game'].str.contains('Bravo')


X = data[~remove]
# Extract the feature columns, remove discussion section
X = X[X['game'].str.contains('Speaker')]
X = X.iloc[:, :-1]

# Standardize the features
# Create an object of StandardScaler which is present in sklearn.preprocessing
scalar = StandardScaler()
scaled_data = pd.DataFrame(scalar.fit_transform(X))  # scaling the data
scaled_data

heatmap = sns.heatmap(scaled_data.corr(), cmap='coolwarm')
# Save the plot to a file
heatmap.figure.savefig('heatmap.png')

# Fit a PCA model to the data
pca = PCA()
pca.fit(scaled_data)

# Calculate the cumulative sum of explained variances
cumulative_var = np.cumsum(pca.explained_variance_ratio_)

# Determine the number of PCs needed to explain > 60% variance
n_components = np.argmax(cumulative_var >= 0.60)+1
n_components

# Create FactorAnalysis object
fa = FactorAnalysis(n_components=n_components, rotation='varimax')
# fa = FactorAnalysis(n_components=n_components, rotation='quartimax')
# quartimax
# varimax

fa.fit(scaled_data)
# Extract the factor loadings
# Inspect the loadings of each variable on each principal component
loadings_df = pd.DataFrame(fa.components_.T, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6'], index=X.columns)
# print(loadings)

loadings = fa.components_.T
# Keep variables with primary loadings > 0.5 and secondary loadings < 0.3
selected_vars = []
for i in range(loadings.shape[0]):
    primary_loading = max(abs(loadings[i, :]))
    secondary_loading = sorted(abs(loadings[i, :]))[-2]
    if primary_loading > 0.5 and secondary_loading < 0.3:
        selected_vars.append(i)

# Keep only the selected variables in the data
X_selected = loadings_df.iloc[selected_vars, :]


# Define a function to find the PC and value for the highest absolute loading
def get_highest_loading(row):
    highest_loading_pc = row.abs().idxmax()
    highest_loading_value = row[highest_loading_pc]
    return pd.Series([highest_loading_pc, highest_loading_value], index=['PC', 'Value'])


# Apply the function to each row of the loading table
loading_table_with_pc = X_selected.apply(get_highest_loading, axis=1)

# Add the new columns to the original loading table
loading_table = pd.concat([X_selected, loading_table_with_pc], axis=1)

# Sort the result DataFrame by the absolute value of the loadings within each PC group
loading_table_with_pc = loading_table_with_pc.sort_values(['PC', 'Value'], ascending=[True, False])

loading_table_with_pc.to_csv('grouped_vars_varimax.csv', index=True)

# loading_table_with_pc.to_csv('grouped_vars_quartimax.csv', index=True)

# varimax and quartimax yeilds to same group result