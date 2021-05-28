import os
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('input_csv_path',   default="../data/result/Qualification_Test_2_GT.csv",   help='AMT result csv')
    parser.add_argument('template_csv_path',default="./check_annotation_template.html",                 help='Path to template html')
    parser.add_argument('save_dir',         default="./qualification_test_2_gt/",                            help='Path to save the video')
    parser.add_argument('--video_line',     default=2749,                                               help='Line to embed video URL in template HTML')
    parser.add_argument('--annot_line',     default=2779,                                               help='Line to embed annotation data in template HTML')

    args = parser.parse_args()

    vid_line = args.video_line
    annot_line = args.annot_line

    # Load AMT Result CSV
    df = pd.read_csv(args.input_csv_path)

    for idx in range(len(df)):
        # Open template file
        with open(args.template_csv_path, 'r', encoding="utf_8") as f:
            lines = f.readlines()

        vid_url = df['Input.video_url_mp4'][idx]
        tag = df['Answer.annotationText'][idx].split('|')
        start = df['Answer.startTimeList'][idx].split('|')
        end = df['Answer.endTimeList'][idx].split('|')

        # Replace video url
        lines[vid_line] = vid_url + '\n'

        # Format for annotation
        fmt = '<div id="annot{i}"><input class="annotationTimeList" type="text" name="startTimeList" readonly="readonly" value="{start}"><input class="annotationTimeList" type="text" name="endTimeList" readonly="readonly" value="{end}"><input id="annotationText" class="annotationTimeList" rows="1" type="text" name="annotationText" value="{tag}" style="width: 200px; font-family:" courier="" new"=""><label>{i}</label><br><input value="|&lt;&lt; Start" onclick="gotoStartAnnot(&#39;annot{i}&#39;)" type="button" "=""><input value="Play" onclick="playSelection(&#39;annot{i}&#39;)" type="button" "=""><input value="Edit" onclick="editAnnotation(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="Delete" onclick="removeAnnotate(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="End &gt;&gt;|" onclick="gotoEndAnnot(&#39;annot{i}&#39;)" type="button" "=""><hr></div>'

        # Insert the line for annotation
        for i in range(1, len(tag)):
            annot_txt = fmt.format(i=i, tag=tag[i], start=start[i], end=end[i])
            lines.insert(annot_line + i, annot_txt+'\n')

        # Save
        if not os.path.exists(args.save_dir):
            os.makedirs(args.save_dir)
        save_path = args.save_dir + df['WorkerId'][idx] + '_' + os.path.basename(vid_url[:-4]) + '.html'
        with open(save_path, 'wt', encoding="utf-8") as f:
            for ele in lines:
                f.write(ele)




