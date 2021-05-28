import os
import glob
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm

data_path = 'C:/Users/b19.teshima/Documents/Gesture/3D-Pose-Baseline-LSTM/data/TED_gesture_dataset_3D_interpolate.pickle'
annotation_dir = "./data/result_csv/Result_20210528"  # The path to folder that include csv files from AMT
save_path_xlsx = "./data/annotation_results_20210528.xlsx"

data = torch.load(data_path)

save_data = {
    'Worker ID':[], 
    'Video ID':[], 
    'Gesture ID':[], 
    'Text':[], 
    'Gesture Type':[], 
    'Remarks':[], 
    'Start Time':[], 
    'End Time':[], 
    'Duration':[]
    }

for f in tqdm(glob.glob(annotation_dir + '/*.csv')):
    df = pd.read_csv(f)
    for i in range(len(df)):
        # load worker ID
        worker_id = df['WorkerId'][i]

        # load video ID
        video_url = df['Input.video_url_mp4'][i]
        video_id = os.path.basename(video_url)[:-4]

        # load gesture type
        gesture_type_text = df['Answer.annotationText'][i]
        gesture_type_list = gesture_type_text.split('|')[1:]
        gt_list = []
        remarks = []
        for gt in gesture_type_list:
            if 'Imagistic' in gt:
                gt_list.append('Imagistic')
                remarks.append(gt[gt.find('(')+1:-1])
            else:
                gt_list.append(gt)
                remarks.append(None)

        # load start times
        start_time_text = df['Answer.startTimeList'][i]
        start_time_list = start_time_text.split('|')[1:]
        start_time_list = [float(t) for t in start_time_list]

        # load end times
        end_time_text = df['Answer.endTimeList'][i]
        end_time_list = end_time_text.split('|')[1:]
        end_time_list = [float(t) for t in end_time_list]

        # assign gesture ID
        gesture_id = []
        for i in range(len(gesture_type_list)):
            gesture_id.append(video_id + '_' + str(i))

        # text data
        for j in range(len(gesture_type_list)):

            yt_video_id = video_id[0:11]
            clip_id = int(video_id[12:])
            isFound = False
            for d in data:
                if yt_video_id == d['vid']:
                    clip_data = d['clips'][clip_id]
                    isFound = True
                    break

            if not isFound:
                print("{} Not Found".format(gesture_id))
                continue
            
            start = start_time_list[j]
            end = end_time_list[j]

            text = ""
            offset = clip_data['start_frame_no']
            for w in clip_data['words']:
                s = max((w[1] - offset) / 25, 0)
                e = max((w[2] - offset) / 25, 0)
                if end <= s:
                    break
                if start <= e:
                    text += w[0] + ' '
            
            # save as csv file
            save_data['Worker ID'].append(worker_id)
            save_data['Video ID'].append(video_id)
            save_data['Gesture ID'].append(gesture_id[j])
            save_data['Text'].append(text)
            save_data['Gesture Type'].append(gt_list[j])
            save_data['Remarks'].append(remarks[j])
            save_data['Start Time'].append(start_time_list[j])
            save_data['End Time'].append(end_time_list[j])
            save_data['Duration'].append(end_time_list[j] - start_time_list[j])
        
save_df = pd.DataFrame(save_data)
save_df.to_excel(save_path_xlsx, index=False)

print("Saved annotation file to {}".format(save_path_xlsx))