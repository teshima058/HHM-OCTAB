import os
import subprocess
import glob

if __name__ == '__main__':
    openpose_path = "D:/Program Files/openpose-1.4.0-win64-gpu-binaries"
    video_dir = "D:/TED_videos/VideoStorage/clip_videos"
    save_json_dir = "D:/TED_videos/VideoStorage_processed/clip_videos"

    cd = os.getcwd()
    os.chdir(openpose_path)

    for vid_folder in glob.glob(video_dir + '/**/'):
        youtube_id = os.path.basename(os.path.dirname(vid_folder))

        for vid in glob.glob(vid_folder + '/*.mp4'):
            video_id = os.path.basename(vid)[:-4]
            each_save_dir = save_json_dir + '/' + youtube_id + '/' + video_id + '/json/'

            if not os.path.exists(each_save_dir):
                os.makedirs(each_save_dir)

            # call bin\OpenPoseDemo.exe --video %video% --write_images %imgs_dir% --write_json %pose_dir% --no_gui_verbose -display 0 -render_pose 2 --number_people_max 1 
            exe = []
            exe.append('bin\\OpenPoseDemo.exe')
            exe.append('--video')
            exe.append(vid)
            exe.append('--write_json')
            exe.append(each_save_dir)
            # exe.append('--write_images')
            # exe.append(save_image_path)
            exe.append('--render_pose')
            exe.append('0')
            exe.append('--no_gui_verbose')
            exe.append('-display')
            exe.append('0')
            exe.append('--number_people_max')
            exe.append('2')
            exe.append('--num_gpu')
            exe.append('1')
            exe.append('--num_gpu_start')
            exe.append('0')

            print(' '.join(exe))
            subprocess.call(' '.join(exe), shell=True)

    os.chdir(cd)


