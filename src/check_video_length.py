import cv2
import pandas as pd
import numpy as np
from tqdm import tqdm

csv_path = "../data/input/input_{}.csv"

video_infos, non_video_nums = [], []
for i in tqdm(range(1, 8)):
    df = pd.read_csv(csv_path.format(i))
    non_video_num = 0
    video_length = []
    for j in range(len(df)):
        
        cap = cv2.VideoCapture(df["video_url_mp4"].iloc[j])
        video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            non_video_num += 1
            continue
        video_len_sec = video_frame_count / video_fps 
        video_length.append(video_len_sec)
    video_infos.append(video_length)
    non_video_nums.append(non_video_nums)

video_infos = np.array(video_infos)
non_video_nums = np.array(non_video_nums)

for i in range(len(video_infos)):
    print("{}\t Sum: {},\t\t Average: {}\t\t None-Video: {}".format(i, np.sum(video_infos[i]), np.mean(video_infos[i]), non_video_nums[i])))

print()