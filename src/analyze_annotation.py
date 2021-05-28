import os
import shutil
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import word_tokenize

import torch
from transformers import BertTokenizer, BertModel

def checkTagFrequency(df, save_dir):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    tag_dic = {}
    for i in range(len(df)):
        if pd.isnull(df['Remarks'].iloc[i]):
            continue

        text = df['Remarks'].iloc[i]
        token = nltk.word_tokenize(text)
        tag = nltk.pos_tag(token)

        for t in tag:
            if t[1] in tag_dic.keys():
                tag_dic[t[1]] += 1
            else:
                tag_dic[t[1]] = 1

    tag_df = pd.DataFrame(tag_dic,index=['i',])
    # print(nltk.help.upenn_tagset())
    # print(tag_df)
    df.T.to_excel(save_dir + 'tag.xlsx')
    print('')


def checkWordFrequency(df, save_dir):
    dic = {}
    for i in range(len(df)):
        text = df['Remarks'].iloc[i] 
        if pd.isna(text):
            continue
        word_tokenize_list = word_tokenize(text)
        for w in word_tokenize_list:
            w = str.lower(w)
            if not w in dic.keys():
                dic[w] = 1
            else:
                dic[w] += 1
    word_list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    word_list = pd.DataFrame(word_list)
    word_list = word_list.rename(columns={0: 'word', 1:'frequency'})

    word_list.to_excel(save_dir + 'word_count.xlsx')


def checkSameWordVideos(df, word, video_dir, save_dir):
    g_ids = []
    remarks = []
    for i in range(len(df)):
        if pd.isna(df['Remarks'][i]):
            continue
        if word in str.lower(df['Remarks'][i]).split():
            remarks.append(df['Remarks'][i])
            g_ids.append(df['Gesture ID'][i])
    
    save_dir += word + '/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i,id in enumerate(g_ids):
        video_path = video_dir + id[:11] + '/' + id + '/' + id + '.mp4'
        if os.path.exists(video_path):
            remarks[i] = remarks[i].replace(' ', '_')
            remarks[i] = remarks[i].replace('.', '')
            remarks[i] = remarks[i].replace('?', '')
            remarks[i] = remarks[i].replace('!', '')
            copy_path = save_dir + id + '_' + remarks[i] + '.mp4'
            shutil.copyfile(video_path, copy_path)

    print()

def checkImagisticRemarkVector(df):

    text = 'I have a pen'

    # Preliminaries
    options_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(options_name)
    bert_model = BertModel.from_pretrained(options_name)
    bert_model.eval()

    texts, vectors = [], []
    for text in df["Remarks"]:
        if pd.isna(text):
            continue

        tokenized_text = tokenizer.tokenize(text)
        tokenized_text.insert(0, "[CLS]")
        tokenized_text.append("[SEP]")
        tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
        tokens_tensor = torch.tensor([tokens])

        with torch.no_grad(): # 勾配計算なし
            all_encoder_layers = bert_model(tokens_tensor)

        embedding = all_encoder_layers[0]
        cls = embedding[:,0,:][0].numpy()

        texts.append(text)
        vectors.append(cls)
    vectors = np.array(vectors)

    # t-SNE for visualization
    X = TSNE(n_components=2, random_state=0).fit_transform(vectors)

    for i in range(len(texts)):
        plt.plot(X[i][0], X[i][1], '')
        plt.annotate(texts[i], xy=(X[i][0], X[i][1]), size=8)

    plt.title("BERT embedding visualization")
    plt.show()



if __name__ == '__main__':
    video_dir = "D:/TED_videos/segmented_by_gesture/"
    xlsx_path = "../data/annotation_results_.xlsx"
    save_dir = '../data/annotation_data/'

    df = pd.read_excel(xlsx_path)

    # checkTagFrequency(df, save_dir)

    # checkWordFrequency(df, save_dir)

    # checkSameWordVideos(df, 'here', video_dir, save_dir)

    checkImagisticRemarkVector(df)






