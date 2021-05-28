import os
import shutil
import pandas as pd

annotation_file = "./data/annotation_results_integrated_20210528.xlsx"
video_dir = "D:/TED_videos/VideoStorage/clip_videos"
save_video_dir = "D:/TED_videos/VideoStorage_annotated"

annot_df = pd.read_excel(annotation_file)

for i in range(len(annot_df)):
    video_id = annot_df['Video ID'].iloc[i][0:11]
    video_path = video_dir + '/' + video_id + '/' + annot_df['Video ID'].iloc[i] + '.mp4'
    if not os.path.exists(video_path):
        continue
    
    each_video_dir = save_video_dir + '/' + video_id
    if not os.path.exists(each_video_dir):
        os.makedirs(each_video_dir)
    
    shutil.move(video_path, each_video_dir)
    print('moved {}'.format(video_path))
