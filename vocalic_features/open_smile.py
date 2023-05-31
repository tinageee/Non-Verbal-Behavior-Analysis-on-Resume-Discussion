import os
import pandas as pd
import opensmile


# set the paths to the input files, the OpenSMILE config file, and the output folder
input_folder = '/Users/saiyingge/Resume_Study_DATA/Unzips-all/mp3/'

# initialize the pyopensmile extractor
extractor = opensmile.Smile(
    # eGeMAPSv02
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)

# create an empty list to store the extracted features
features = pd.DataFrame()


# loop over the MP3 files in the input folder
for file_name in os.listdir(input_folder):
    # for intro and note stage only
    if file_name.endswith('.mp3') and 'Speaker' in file_name:
        print(file_name)
        # extract the audio features from the current file
        file_path = os.path.join(input_folder, file_name)
        result = extractor.process_file(file_path)
        result = result.assign(game=file_name)

        # append the features to the list
        features = pd.concat([features, result], ignore_index=True)

# # convert the list of features to a pandas dataframe
# df = pd.DataFrame(features)

# save the features to CSV file in the output folder
output_file = os.path.join('raw_features.csv')
features.to_csv(output_file, index=False)
