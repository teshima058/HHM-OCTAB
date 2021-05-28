import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm


def extractAnnotationInfo(data):
    start_time_list = data['Answer.startTimeList'].split('|')[1:]
    end_time_list = data['Answer.endTimeList'].split('|')[1:]
    annot_list = data['Answer.annotationText'].split('|')[1:]
    video_url = data['Input.video_url_mp4']
    video = cv2.VideoCapture(video_url)
    count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    annot_info = np.zeros(int(count+1))
    segment_info = np.zeros(int(count+1))
    for i in range(len(annot_list)):
        start_frame = int(fps * float(start_time_list[i]))
        end_frame = int(fps * float(end_time_list[i]))
        segment_info[end_frame] = 1
        for j in range(start_frame, end_frame+1):
            if annot_list[i] == 'No-Gesture':
                annot_info[j] = 1
            elif annot_list[i] == 'Beat':
                annot_info[j] = 2
            elif 'Imagistic' in annot_list[i]:
                annot_info[j] = 3
    return annot_info, segment_info

if __name__ == "__main__":

    # Each Path
    gt_csv_path = "../data/result/Qualification_Test_2_GT.csv"
    worker_csv_path = "../data/result/Qualification_Test_2.csv"
    save_xlsx = "./qualification_test_2/workers_score_qt2.xlsx"

    print("Loading CSV...")
    gt_df = pd.read_csv(gt_csv_path)
    worker_df = pd.read_csv(worker_csv_path)

    gt_data = {}
    for i in range(len(gt_df)):
        annot_info, segment_info = extractAnnotationInfo(gt_df.iloc[i])
        data = {
            "annot_info"    : annot_info,
            "segment_info"  : segment_info
        }
        gt_data[gt_df['Input.video_url_mp4'][i]] = data

    print("Calculating each score...")
    workers_score = {}
    worker_list, video_list, annot_list, segment_list, sum_list = [], [], [], [], []
    for i in tqdm(range(len(worker_df))):

        # if not (os.path.basename(worker_df['Input.video_url_mp4'][i])[:-4] == "xukDIWFMU9Y_2" 
        #     and worker_df['WorkerId'][i] == "A1BLIXWAGK65TZ"):
        #     continue

        annot_gt = gt_data[worker_df['Input.video_url_mp4'][i]]['annot_info']
        segment_gt = gt_data[worker_df['Input.video_url_mp4'][i]]['segment_info']
        video_url = worker_df['Input.video_url_mp4'][i]
        video = cv2.VideoCapture(video_url)
        fps = video.get(cv2.CAP_PROP_FPS)

        annot, segment = extractAnnotationInfo(worker_df.iloc[i])

        # Annotation Score
        correct_num = np.count_nonzero(annot == annot_gt)
        annot_score = correct_num / len(annot)

        # Segmentation Score
        segment_score = 0
        for j in range(len(segment_gt)):
            if segment_gt[j] != 1:
                continue
            closest_frame = fps
            for k in range(int(j-fps), int(j+fps)):
                if k < 0 or k >= len(segment):
                    continue
                if segment[k] == 1 and closest_frame > abs(j-k):
                    closest_frame = abs(j-k)
            segment_score += closest_frame / fps
        segment_score = segment_score / np.count_nonzero(segment_gt == 1)
        
        # Penalty of the difference of segment num
        penalty = abs(np.count_nonzero(segment_gt == 1) - np.count_nonzero(segment == 1))
        penalty = penalty / (np.count_nonzero(segment_gt == 1) + np.count_nonzero(segment == 1))

        segment_score = 1 - (segment_score + penalty) / 2

        worker_list.append(worker_df['WorkerId'][i])
        video_list.append(os.path.basename(video_url[:-4]))
        annot_list.append(annot_score)
        segment_list.append(segment_score)
        sum_list.append(annot_score + segment_score)

    print("Saving to {} ...".format(save_xlsx))

    # Score of each video
    videos_score = pd.DataFrame({
        "Worker ID" : worker_list,
        "Video ID" : video_list,
        "Annotation Score" : annot_list,
        "Segmentation Score" : segment_list,
        "Sum of Score" : sum_list
    })

    # Score of each worker
    workers_list, annot_list, segment_list, sum_list = [], [], [], []
    for i in range(len(videos_score)):
        if not videos_score['Worker ID'][i] in workers_list:
            w_df = videos_score[videos_score['Worker ID'] == videos_score['Worker ID'][i]]
            workers_list.append(videos_score['Worker ID'][i])
            annot_list.append(w_df.mean()['Annotation Score'])
            segment_list.append(w_df.mean()['Segmentation Score'])
            sum_list.append(w_df.mean()['Sum of Score'])
    workers_score = pd.DataFrame({
        "Worker ID": workers_list, 
        "Annotation Score" : annot_list,
        "Segmentation Score" : segment_list,
        "Sum of Score": sum_list})

    with pd.ExcelWriter(save_xlsx) as writer:
        workers_score.to_excel(writer, sheet_name="workers_score", index=False)
        videos_score.to_excel(writer, sheet_name="videos_score", index=False)

    print("Finish.")