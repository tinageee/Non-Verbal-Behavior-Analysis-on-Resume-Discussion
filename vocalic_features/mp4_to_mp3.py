import os
import subprocess

#add missing mp3 file

# Note - SG4111,SG4121,SG4122,SG4131,SG415A(only 2)
missing_files = ['SG4111','SG4121','SG4122','SG4131','SG415A','XW418A','SG415B','XC411A']

# set the input and output file paths
input_folder = '/Users/saiyingge/Resume_Study_DATA/Unzips-all/mp4/'
output_folder = '/Users/saiyingge/Resume_Study_DATA/Unzips-all/mp3/'


for file_name in os.listdir(input_folder):
    if file_name.endswith('.mp4') and 'Note' in file_name \
            and any(missing_file in file_name for missing_file in missing_files):
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp3')

        if os.path.isfile(output_file):
            print(f"Output file '{output_file}' already exists and was not overwritten")
        else:

            # extract the audio features from the current file
            # run the ffmpeg command to convert the file
            subprocess.run(
                ['ffmpeg', '-i', input_file, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', output_file],
                check=True)

