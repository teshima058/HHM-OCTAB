import os
import glob
import pandas as pd

url_prefix = 'https://teshima058.github.io/VideoStorage/clip_videos/'
video_dir = "../VideoStorage/clip_videos/"
save_path = './data/input_test.csv'

dic = { 'video_url_mp4_compare'     :[], 
        'video_url_webm_compare'    :[], 
        'start_time'                :[], 
        'end_time'                  :[], 
        'title'                     :[], 
        'gt_start_times'            :[], 
        'gt_end_times'              :[], 
        'gt_tags'                   :[], 
        'video_url_mp4'             :[], 
        'video_url_webm'            :[]}


video_urls, none_list = [], []
for each_video_dir in glob.glob(video_dir + "**/"):
    video_id = os.path.basename(each_video_dir[:-1])
    for video in glob.glob(each_video_dir + '*.mp4'):
        video_name = os.path.basename(video)
        url = url_prefix + video_id + '/' + video_name
        video_urls.append(url)
        none_list.append(None)

dic['video_url_mp4_compare' ] = none_list
dic['video_url_webm_compare'] = none_list
dic['start_time'            ] = none_list
dic['end_time'              ] = none_list
dic['title'                 ] = none_list
dic['gt_start_times'        ] = none_list
dic['gt_end_times'          ] = none_list
dic['gt_tags'               ] = none_list
dic['video_url_mp4'         ] = video_urls
dic['video_url_webm'        ] = none_list


df = pd.DataFrame(dic)
df.to_csv(save_path, index=False)

print("Finish")