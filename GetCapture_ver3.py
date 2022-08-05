import requests
from bs4 import BeautifulSoup
import os
import sys
import csv
import glob
import pandas as pd
import hashlib

if len(sys.argv) < 3:
    try:
        os.mkdir("img")
        DIR = "img"
    except:
        pass
else:
    try:
        os.mkdir(sys.argv[2])
        DIR = sys.argv[2]
    except:
        pass
URL = sys.argv[1]
images = []
soup = BeautifulSoup(requests.get(URL).content,'lxml')
for link in soup.find_all("img"):
    if link.get("data-src"):
        data_src = link.get("data-src")
        if data_src.endswith(".jpg"):
            images.append(link.get("data-src"))
for target in images:
    if target.startswith("http"):
        tag = target
    else:
        tag = URL + '/' + target
    re = requests.get(tag)
    with open(DIR + '/' + tag.split('/')[-1], 'wb') as f:
        f.write(re.content)
list_path = os.getcwd() + '\\' + DIR
csv_file = list_path + "\list.csv"
file_list = glob.glob(list_path + "/*")
data_list = []
for i, file_path in enumerate(file_list, start=1):
    file_size = os.path.getsize(file_path)
    hash_sha256 = hashlib.sha256(file_path.encode("utf-8")).hexdigest()
    data_list.append([i,os.path.basename(file_path),file_size,hash_sha256])
    column_list = ['No', 'File_name', 'File_size', 'Hash_sha256']
    df = pd.DataFrame(data_list, columns = column_list)
    df.to_csv(csv_file, sep=',', index=False, encoding='utf-8')

print("Save to 【" + list_path + "】")
