import os
import glob
import subprocess
import numpy as np
import pandas as pd
import argparse
from tqdm import tqdm


if __name__ == '__main__':

    annotation_xlsx = "../data/annotation_results.xlsx"
    original_video_dir = "D:/TED_videos/VideoStorage/clip_videos/"
    save_video_dir = "D:/TED_videos/segmented_by_gesture/"

    df = pd.read_excel(annotation_xlsx)

    # Correct all labanotation json path
    video_gestures = []
    video_nums = 0
    for raw_video in tqdm(glob.glob(original_video_dir + '**/')):
        video_id = os.path.basename(raw_video[:-1])
        for clip in glob.glob(raw_video + '*.mp4'):
            clip_id = os.path.basename(clip[:-4])
            annot = df[df['Video ID'] == clip_id]
            for i in range(len(annot)):
                start = annot['Start Time'].iloc[i]
                duration = annot['Duration'].iloc[i]
                gesture_id = annot['Gesture ID'].iloc[i]

                save_dir = save_video_dir + video_id + '/' + gesture_id + '/'
                save_path = save_dir + gesture_id + '.mp4'
                if os.path.exists(save_path):
                    continue

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                print('Saved to {}'.format(save_path))
                cmd = []
                cmd.append('ffmpeg')
                cmd.append('-ss')
                cmd.append(str(start))
                cmd.append('-i')
                cmd.append(clip)
                cmd.append('-t')
                cmd.append(str(duration))
                cmd.append(save_path)
                cmd.append('-y')
                subprocess.call(cmd)



