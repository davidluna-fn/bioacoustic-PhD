import os
import math
import torch
import datetime
import numpy as np
import pandas as pd
import soundfile as sf
from pathlib import Path
from torch.utils.data import Dataset, DataLoader


class EcoDataTesis(Dataset):

    def __init__(self,root_path,path_labels,path_names,ext):

        self.root_path = root_path
        self.files = []
        self.pd_labels = pd.read_excel(path_labels)
        self.pd_files = pd.read_excel(path_names)

        for i in range(len(self.pd_files['Carpetas'].values)):
          path_aux = "{}/{}".format(root_path, self.pd_files['Carpetas'].iloc[i])
          self.files+=list(Path(path_aux).rglob("*.{}".format(ext)))


    def __getitem__(self, index):
        path_index = self.files[index]
        split_filename = str(path_index).split("/")
        split_filename = split_filename[len(self.root_path.split("/")):]

        if split_filename[0] == 'Guajira_2016':
            serial = int(split_filename[2].split("_")[-1][2:])
            date = int(split_filename[-1].split('_')[1])
            labels_file = self.pd_labels[self.pd_labels['Departamento'] == split_filename[0]]

        elif split_filename[0] == 'Caribe':
            serial = int(split_filename[2])
            date = int(split_filename[3])
            labels_file = self.pd_labels.copy()

        labels_file = labels_file[labels_file['Serial Songmeter'] == serial]

        for i in range(len(labels_file)):
            date_ini = int(labels_file["Fecha Inicio"].iloc[i])
            date_end = int(labels_file["Fecha Final"].iloc[i])
            if date_ini <= date <= date_end:
                features = {"transform": labels_file["Transformación"].iloc[i], "Latitud": labels_file["Latitud"].iloc[i],
                            "Longitud": labels_file["Longitud"].iloc[i], "Permanencia": labels_file["Permanencia"].iloc[i]}
                break
            else:
                continue

        record, sr = sf.read(path_index)
        return record, sr, features  

    def __len__(self):
        return len(self.files)