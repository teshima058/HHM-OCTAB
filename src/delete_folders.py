import os
import glob
import shutil

video_dir = "D:/TED_videos/VideoStorage/clip_videos"

for each_video_dir in glob.glob(video_dir + "/**/"):
    video_id = os.path.basename(each_video_dir[:-1])

    for folder in glob.glob(each_video_dir + '/**/'):
        try:
            shutil.rmtree(folder)
        except OSError:
            for i in range(100):
                try:
                    if os.path.exists(folder):
                        os.rmdir(folder)
                    else:
                        break
                except OSError:
                    continue

            print(folder)
            print()