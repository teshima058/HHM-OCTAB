import os
import pandas as pd

csv_path = "../data/result/Batch_4340351_batch_results.csv"
template_path = "./confirm_annotation_template.html"
save_dir = "./confirm_annotation/"
vid_line = 2749
annot_line = 2779

df = pd.read_csv(csv_path)

for idx in range(len(df)):
    
    with open(template_path, 'r', encoding="utf_8") as f:
        lines = f.readlines()

    vid_url = df['Input.video_url_mp4'][idx]
    tag = df['Answer.annotationText'][idx].split('|')
    start = df['Answer.startTimeList'][idx].split('|')
    end = df['Answer.endTimeList'][idx].split('|')

    fmt = '<div id="annot{i}"><input class="annotationTimeList" type="text" name="startTimeList" readonly="readonly" value="{start}"><input class="annotationTimeList" type="text" name="endTimeList" readonly="readonly" value="{end}"><input id="annotationText" class="annotationTimeList" rows="1" type="text" name="annotationText" value="{tag}" style="width: 200px; font-family:" courier="" new"=""><label>{i}</label><br><input value="|&lt;&lt; Start" onclick="gotoStartAnnot(&#39;annot{i}&#39;)" type="button" "=""><input value="Play" onclick="playSelection(&#39;annot{i}&#39;)" type="button" "=""><input value="Edit" onclick="editAnnotation(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="Delete" onclick="removeAnnotate(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="End &gt;&gt;|" onclick="gotoEndAnnot(&#39;annot{i}&#39;)" type="button" "=""><hr></div>'

    lines[vid_line] = vid_url + '\n'

    for i in range(1, len(tag)):
        annot_txt = fmt.format(i=i, tag=tag[i], start=start[i], end=end[i])
        lines.insert(annot_line + i, annot_txt+'\n')

    save_path = save_dir + os.path.basename(vid_url[:-4]) + '_' + df['WorkerId'][idx] + '.html'
    with open(save_path, 'wt', encoding="utf-8") as f:
        for ele in lines:
            f.write(ele)




