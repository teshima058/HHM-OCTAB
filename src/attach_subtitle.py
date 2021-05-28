import os
import cv2
import subprocess
import pickle
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageFont, ImageDraw

# 画像に文字を入れる関数
def telop(img, message, W, H):
    font_path = 'C:\Windows\Fonts\meiryo.ttc'        # Windowsのフォントファイルへのパス
    img = Image.fromarray(img)                       # cv2(NumPy)型の画像をPIL型に変換
    draw = ImageDraw.Draw(img)                       # 描画用のDraw関数を用意
    if W == 1280:
        font_size = 48                               # フォントサイズ
    elif W == 640:
        font_size = 24
    font = ImageFont.truetype(font_path, font_size)  # PILでフォントを定義

    w, h = draw.textsize(message, font)              # .textsizeで文字列のピクセルサイズを取得

    # テロップの位置positionは画像サイズと文字サイズから決定する
    # 横幅中央、縦は下
    position = (int((W - w) / 2), int(H - (font_size * 1.5)))

    # 中央揃え
    #position = (int((W - w) / 2), int((H - h) / 2))

    # テキストを描画（位置、文章、フォント、文字色(BGR+α)を指定）
    draw.text(position, message, font=font, fill=(255, 255, 255, 0))

    # PIL型の画像をcv2(NumPy)型に変換
    img = np.array(img)
    return img

# 動画を読み込み1フレームずつ画像処理をする関数
def m_slice(path, message, save_path, step=1):
    in_path = path                                      # 読み込みパスを作成
    movie = cv2.VideoCapture(in_path)                   # 動画の読み込み
    Fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))       # 動画の全フレーム数を計算
    fps = movie.get(cv2.CAP_PROP_FPS)                   # 動画のFPS（フレームレート：フレーム毎秒）を取得
    W = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))        # 動画の横幅を取得
    H = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))       # 動画の縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # 動画保存時のfourcc設定（mp4用）

    # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
    video = cv2.VideoWriter(save_path, fourcc, int(fps / step), (W, H))
    ext_index = np.arange(0, Fs, step)  # 動画から静止画（フレーム）を抽出する間隔

    j = 0                               # message配列から文章と時間を抜き出す指標番号
    section = message[j]                # フレームに書き込む文章と時間の初期値
    print("adding subtitles...")
    for i in tqdm(range(Fs)):                 # フレームサイズ分のループを回す
        flag, frame = movie.read()      # 動画から1フレーム読み込む
        check = i == ext_index          # 現在のフレーム番号iが、抽出する指標番号と一致するかチェックする
        time = i / int(fps/step)        # 抽出したフレームの動画内経過時間

        if flag == True: # フレームを取得できた時だけこの処理をする
            # もしi番目のフレームが静止画を抽出するものであれば、ファイル名を付けて保存する
            if True in check:
                # ここから動画フレーム処理と動画保存---------------------------------------------------------------------
                # 抽出したフレームの再生時間がテロップを入れる時間範囲に入っていれば文字入れする
                if section[1] <= time <= section[2]:
                    frame = telop(frame, section[0], W, H)  # テロップを入れる関数を実行
                # 再生時間がテロップ入れ開始時間より小さければ待機する
                elif section[1] > time:
                    pass
                else:
                    # 用意した文章がなくなったら何もしない
                    if j >= len(message) - 1:
                        pass
                    # 再生時間範囲になく、まだmessage配列にデータがある場合はjを増分しsectionを更新
                    else:
                        j = j + 1
                        section = message[j]
                video.write(frame)                          # 動画を1フレームずつ保存する
            # ここまでが動画フレーム処理と保存---------------------------------------------------------------------
            # i番目のフレームが静止画を抽出しないものであれば、何も処理をしない
            else:
                pass
        else:
            pass
    return


def video2wav(video_file, wav_file):
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {} -y".format(video_file, wav_file)
    subprocess.call(command, shell=True)


def attachWav(video_file, wav_file, save_path):
    cmd = "ffmpeg -i {mp4} -i {wav} -c:v copy -c:a aac -strict experimental -map 0:v -map 1:a {output} -y".format(
        mp4=video_file, wav=wav_file, output=save_path)
    subprocess.call(cmd)


# # [文章, 開始時間, 終了時間]:ここで指定した動画内時間の範囲にテロップ文章を入れる
# # message = [['このように', 1, 4],
# #            ['動画内のアクションの時間さえわかっていれば', 4.5, 11],
# #            ['アクションに合わせたテロップを入れることができます', 12, 17]]
def attachSubtitle(video_path, message, save_path):
    # 動画処理の関数を実行・音声なしの動画が出力される
    m_slice(video_path, message, './tmp.mp4')
    # 動画から音声を抽出
    video2wav(video_path, './tmp.wav')
    # 音声を付ける
    attachWav('./tmp.mp4', './tmp.wav', save_path)

    os.remove('./tmp.mp4')
    os.remove('./tmp.wav')

    print('Saved to {}'.format(save_path))


if __name__ == '__main__':

    data_path = r"C:\Users\b19.teshima\Documents\Gesture\OtherMethods\Co-Speech_Gesture_Generation_my\data\ted_gesture_dataset_train.pickle"
    video_dir = 'D:/TED_videos/VideoStorage/clip_videos/'
    save_dir = 'D:/TED_videos/VideoStorage/clip_videos_subtitle/'
    max_char = 35               # 一度に表示する最大文字数
    fps = 25

    with open (data_path, 'rb') as f:
        data = pickle.load(f)

    for i in range(len(data)):
        video_id = data[i]['vid']
        for c_idx,clip in enumerate(data[i]['clips']):
            clip_id = video_id+'_'+str(c_idx)
            video_path = video_dir + video_id + '/' + clip_id + '.mp4'

            if not os.path.exists(video_path):
                continue

            save_each_dir = save_dir + video_id + '/'
            if not os.path.exists(save_each_dir):
                os.makedirs(save_each_dir)
            save_path = save_each_dir + clip_id + '.mp4'

            if os.path.exists(save_path):
                continue

            start_frame = clip['start_frame_no']
            message = []
            word_list = []
            text = ""
            for j,w in enumerate(clip['words']):

                word_list.append(w)
                text += w[0] + ' '

                if len(text) >= max_char or j == len(clip['words']) - 1:
                    start_time = max((word_list[0][1] - start_frame) / fps, 0)
                    end_time = (w[2] - start_frame) / fps
                    message.append([text, start_time, end_time])
                    word_list = []
                    text = ""
            

            # 動画処理の関数を実行
            attachSubtitle(video_path, message, save_path)


