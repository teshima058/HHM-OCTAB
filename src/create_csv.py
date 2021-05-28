import os
import glob
import pandas as pd
import urllib.request, urllib.error
from tqdm import tqdm

def isValidURL(url):
	try:
		f = urllib.request.urlopen(url)
		return True
		f.close()
	except:
		return False

url_prefix = 'https://teshima058.github.io/VideoStorage/clip_videos/'
video_dir = "D:/TED_videos/VideoStorage/clip_videos"
save_dir = './data/input_csv/20210529/'
invalid_txt = "./data/invalid_videos.txt"
worker_num = 5

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

with open(invalid_txt, 'r') as f:
    invalid_videos = f.read().splitlines()

video_urls, none_list = [], []
invalid_urls, urls = 0, 0
for each_video_dir in tqdm(glob.glob(video_dir + "/**/")):
	video_id = os.path.basename(each_video_dir[:-1])
	for video in glob.glob(each_video_dir + '*.mp4'):
		video_name = os.path.basename(video)
		if video_name[:-4] in invalid_videos:
			urls += 1
			invalid_urls += 1
			continue

		url = url_prefix + video_id + '/' + video_name
		if isValidURL(url):
			video_urls.append(url)
			none_list.append(None)
		else:
			invalid_urls += 1
		urls += 1

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

if not os.path.exists(save_dir):
	os.makedirs(save_dir)

each_data_num = int(len(df) / worker_num)
worker_count = 1
for i in range(0, len(df), each_data_num):
	if worker_count == worker_num:
		df_ = df[i:]
		save_path = save_dir + 'input_{}.csv'.format(worker_count)
		df_.to_csv(save_path, index=False)
		break
	else:
		df_ = df[i:i+each_data_num]
		save_path = save_dir + 'input_{}.csv'.format(worker_count)
		df_.to_csv(save_path, index=False)
		worker_count += 1

print("Invalid Videos: {}/{}".format(invalid_urls, urls))
print("Finish")