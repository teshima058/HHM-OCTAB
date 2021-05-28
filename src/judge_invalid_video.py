"""
For excluding the videos with  multi-person detected
"""

import os
import json
import glob
import numpy as np


json_dirs = "D:/TED_videos/VideoStorage_processed/clip_videos"
save_data = "./data/invalid_videos.txt"

invalid_list = []
for youtube_dir in glob.glob(json_dirs + '/**/'):
    for video_dir in glob.glob(youtube_dir + '/**/'):
        video_id = os.path.basename(os.path.dirname(video_dir))

        if video_id != "2j00U6lUC-c_2":
            continue

        json_dir = video_dir + '/json/'
        
        # load json files
        json_files = os.listdir(json_dir)
        # check for other file types
        json_files = sorted([filename for filename in json_files if filename.endswith(".json")])

        isInvalid = False
        multi_person_frames = 0
        for file_name in json_files:
            _file = os.path.join(json_dir, file_name)
            data = json.load(open(_file))
            
            if len(data['people']) >= 2:
                multi_person_frames += 1

        if multi_person_frames / len(json_files) > 0.8:
            invalid_list.append(video_id)

with open(save_data, 'w') as f:
    for vid_id in invalid_list:
        f.write("%s\n" % vid_id)

