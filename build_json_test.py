import json
import os
import pandas as pd
import sys
# path to the output CommonVoice-DEMAND trainset
OUT_ROOT = sys.argv[1]

# path to the original CommonVoice corpus
CV_ROOT = sys.argv[2]

# path to the original VoiceBank-DEMAND corpus
VB_ROOT = sys.argv[3]


OUT_FILE = "%s/test.json"%OUT_ROOT

CLEAN_ROOT = "%s/train_clean"%OUT_ROOT
NOISY_ROOT = "%s/train"%OUT_ROOT

word_info = pd.read_csv("%s/validated.tsv"%CV_ROOT,sep="\t")

with open("%s/test.json"%VB_ROOT) as f: 
    test_dict = json.load(f)

out_dict = {}
new_test_list = os.listdir(NOISY_ROOT)
for f in test_dict:
    print(f)
    f_full = [x for x in new_test_list if f in x]
    if len(f_full) == 0:
        #print("%s not found in new list"%f)
        continue
    print(f_full)
    f_full = f_full[0]
    print(f_full)

    f_og,f_new = f_full.split("@")
    
    print(f_og,f_new)
    clean_path = os.path.join("{data_root}/test_clean_16k/",f_new)
    noisy_path = os.path.join("{data_root}/test_16k/",f_full)
    f_mp3 = f_new.replace(".wav",".mp3")
    words = word_info[word_info["path"]==f_mp3]["sentence"].values[0].upper()
    print(clean_path)
    print(noisy_path)
    print(words)
    out_dict[f.strip(".wav")] = {"clean_wav":clean_path,"noisy_wav":noisy_path,"words":words}
    
with open(OUT_FILE,"w") as f:
    json.dump(out_dict,f,indent=4)