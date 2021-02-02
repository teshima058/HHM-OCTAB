import pandas as pd
from bs4 import BeautifulSoup

csv_path = "../data/result/Batch_307130_batch_results.csv"
html_path = "./confirm_annotation.html"
idx = 2

df = pd.read_csv(csv_path)
soup = BeautifulSoup(open(html_path, encoding="utf-8"), "html.parser")

vid_url = df['Input.video_url_mp4'][idx]
tag = df['Answer.annotationText'][idx].split('|')
start = df['Answer.startTimeList'][idx].split('|')
end = df['Answer.endTimeList'][idx].split('|')

fmt = '<div id="annot{i}"><input class="annotationTimeList" type="text" name="startTimeList" readonly="readonly" value="{start}"><input class="annotationTimeList" type="text" name="endTimeList" readonly="readonly" value="{end}"><input id="annotationText" class="annotationTimeList" rows="1" type="text" name="annotationText" value="{tag}" style="width: 200px; font-family:" courier="" new"=""><label>{i}</label><br><input value="|&lt;&lt; Start" onclick="gotoStartAnnot(&#39;annot{i}&#39;)" type="button" "=""><input value="Play" onclick="playSelection(&#39;annot{i}&#39;)" type="button" "=""><input value="Edit" onclick="editAnnotation(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="Delete" onclick="removeAnnotate(&#39;annotationListInnerArea&#39;, &#39;annot{i}&#39;)" type="button" "=""><input value="End &gt;&gt;|" onclick="gotoEndAnnot(&#39;annot{i}&#39;)" type="button" "=""><hr></div>'

print()
print(vid_url)
print()
for i in range(1, len(tag)):
    annot_txt = fmt.format(i=i, tag=tag[i], start=start[i], end=end[i])
    annot_html = soup.find(id='annotationListOuterArea')
    print(annot_txt) 


