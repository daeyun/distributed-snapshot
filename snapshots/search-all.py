#!/usr/bin/env python3
import os
import sys
import re

current_dir = os.path.dirname(os.path.realpath(__file__))
file_list = [f for f in os.listdir(current_dir) if f.startswith("snapshot.")]

for filename in file_list:
    if len(sys.argv) != 2:
        print('Usage: {} "snapshot 0"'.format(sys.argv[0]))
        exit()

    full_filename = current_dir + '/' + filename
    search_string = sys.argv[1]

    with open(full_filename) as f:
        lines = f.readlines()

    for line in lines:
        if line.find(search_string) > -1:
            print(line, end="")
