import numpy as np 
from collections import defaultdict
import matplotlib.pyplot as plt
import math
import os
import sys

# Read the list of stations from the file "stalst_ILAN"
f = open("./stalst_ILAN").readlines()[:]
sta_list = []
for i in range(len(f)):
        sta_list.append(f[i].split(" ")[0])
        sta_list = sorted(sta_list)

# Create a dictionary to store the file lists for each station
sta_files = {}

# Iterate through all file lists
for sta in sta_list:
        # Initialize the file list for each station
        sta_files[sta] = []
        baz_all = []
        freq_list = []

        # Iterate through the modes in mode_list
        for mode in ["1", "2", "3", "4", "5"]:
                # Construct the file name
                data_file = f"./Sorted_oneday_ILAN/{sta}_mode{mode}_total_Yilan_wlen8.asc"
                # Add the file name to the station's file list
                sta_files[sta].append(data_file)

                try:
                        # Read the lines from the data file
                        lines = open(data_file).readlines()
                        merged_lines = []

                        # Iterate through the lines and merge type 2 lines if type 1 lines are the same
                        for i in range(len(lines)):
                                if len(lines[i].split()) == 6:
                                        merged_lines.append(lines[i])
                                elif len(lines[i].split()) == 7:
                                        if merged_lines and merged_lines[-1] == lines[i]:
                                                continue
                                        merged_lines.append(lines[i])

                        # Write the merged lines to the merged file
                        merged_file = f"./{sta}_mode_all_total_Yilan_wlen8.asc"
                        with open(merged_file, "w") as merged:
                                merged.write("".join(merged_lines))

                        print(f"Merged file created: {merged_file}")
                except:
                        print(f"Error merging files for station {sta}")


#2028_mode1_total_Yilan_wlen8.asc (original)
#2028_mode2_total_Yilan_wlen8.asc (original)
#2028_mode3_total_Yilan_wlen8.asc (original)
#2028_mode4_total_Yilan_wlen8.asc (original)
#2028_mode5_total_Yilan_wlen8.asc (original)
#2028_mode_all_total_Yilan_wlen8.asc (change to)
