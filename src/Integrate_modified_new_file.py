import os
import pandas as pd
import openpyxl as xl
from openpyxl.styles import PatternFill

modified_file = "./data/annotation_results_integrated.xlsx"
new_file = "./data/annotation_results_20210528.xlsx"
save_path = "./data/annotation_results_integrated_20210528.xlsx"

mod_df = pd.read_excel(modified_file)
new_df = pd.read_excel(new_file)
save_df = pd.read_excel(new_file)

for i in range(len(new_df)):
    gesture_id = new_df['Gesture ID'][i]
    if mod_df[mod_df['Gesture ID']==gesture_id].empty:
        continue
    remark = mod_df[mod_df['Gesture ID']==gesture_id].iloc[0]['Remarks']
    gesture_type = mod_df[mod_df['Gesture ID']==gesture_id].iloc[0]['Gesture Type']

    save_df.loc[save_df['Gesture ID']==gesture_id, ['Remarks']] = remark
    save_df.loc[save_df['Gesture ID']==gesture_id, ['Gesture Type']] = gesture_type

save_df.to_excel(save_path, index=False)

print("Saved to {}".format(save_path))