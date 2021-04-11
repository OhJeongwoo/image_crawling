import os
import glob
import shutil
from os import path
import numpy as np

project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
size = 100

result_path = project_path + "/result/"
keywords = np.load(project_path + "/vocab.npy")
save_path = project_path + "/additional_vocab.npy"

rt = []

for i in range(len(keywords)):
    keyword = keywords[i]
    keyword_path = result_path + keyword
    
    if not path.exists(keyword_path):
        print("there is no directory for " + keyword)
        rt.append(keyword)
        continue
    
    files = os.listdir(keyword_path)
    if len(files) < size:
        print("# of files for " + keyword + ": " + str(len(files)))
        rt.append(keyword)
        #shutil.rmtree(keyword_path)

np.save(save_path, rt)