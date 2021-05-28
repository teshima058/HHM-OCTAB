# 各スクリプトの説明

## organize_annotation.py
- AMTで集めた各ワーカーのcsvファイルをどこか一つのフォルダに置く 
- そのフォルダを annotation_dir に指定
- save_xlsx_path にアノテーションをまとめる

## Integrate_modified_new_file.py
- organize_annotation.pyで作成したcsvファイル同士を統合するスクリプト
- 新しくアノテーションファイルを作ったり、注釈を手動で修正した後に、これを使って統合する

## highlighte_errors.py
- organize_annotation.pyで作成したcsvファイルのTextとRemarkが食い違う行をハイライトする
- 手動で修正したい時にハイライトしてから修正する

## check_annotation.py
- アノテーションを確認したい時に入力したcsvを動画ごとにhtmlに起こして一つのフォルダに出力する

## run_openpose.py
- OpenPoseを指定したフォルダにバッチ処理する

## judge_invalid_video.py
- OpenPoseで２人以上検出された動画はInvalidとする
- Invalidな動画はそのIDをinvalid.txtに出力される

## attach_subtitle.py
- 動画に字幕を付けて別の場所に保存する

## move_already_annotated_video.py
- organize_annotation.pyで作成したcsvファイルを見て、すでにアノテーション済みの動画は他の場所に移す
- (Video Storageにアップロードできる動画が限られているため)

## create_csv.py
- 動画がアップロードされているかを確認しつつ、worker_num分のAMTに入力用のcsvファイルを作成する
- invalidな動画は無視



