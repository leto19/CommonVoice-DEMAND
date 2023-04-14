import numpy as np
import soundfile as sf
import pysepm
import csv
import scipy.signal as sps
import pandas as pd
from asl_P56 import asl_P56
import os
import sys
np.random.seed(100)
"""
DEMAND_ROOT = "/home/george/sshfs/18tb_fstore_1/corpora/VoiceBank-DEMAND//DEMAND_48K/"
VOICEBANK_ROOT = "/home/george/sshfs/18tb_fstore_1/corpora/VoiceBank-DEMAND//VoiceBank/"
COMMONVOICE_ROOT = "/home/george/sshfs/18tb_fstore_1/corpora/CommonVoice/french/fr/"
OUTPUT_ROOT = "kermit/18tb_fstore_1/recordings/CommonVoice-FR/"
"""
COMMONVOICE_ROOT = sys.argv[1]
VOICEBANK_ROOT = sys.argv[2]
DEMAND_ROOT = sys.argv[3]
OUTPUT_ROOT = sys.argv[4]

def find_matching(s,fs,used_list):
    other_root = "%s/clips_validated"%COMMONVOICE_ROOT
    other_dur_info = pd.read_csv("%s/clips_validated_len.csv"%COMMONVOICE_ROOT,header=None)
    #filter out the used files
    print(used_list)
    #print(len(other_dur_info))
    other_dur_info = other_dur_info[~other_dur_info[0].isin(used_list)]
    print(len(other_dur_info))

    s_len = len(s)/fs
    #find the closest match
    other_dur_info["diff"] = np.abs(other_dur_info[1]-s_len)
    
    other_name = other_dur_info[other_dur_info["diff"]==other_dur_info["diff"].min()][0].values[0]
    other_path = os.path.join(other_root,other_name)
    other,fs = sf.read(other_path)
  
    return other,other_path

def resample(s,fs,new_rate):
    number_of_samples = round(len(s) * float(new_rate) / fs)
    s_resamp = sps.resample(s, number_of_samples)
    return s_resamp

def simulate(s_name,v_name,snr,used_list):
    v = v_name
    old_name = s_name.split("/")[-1] #basename of the speech file    
    s_old,fs = sf.read(s_name) # read the speech audio file
    
    s, s_path = find_matching(s_old,fs,used_list)
    new_name = s_path.split("/")[-1] #basename of the speech file

    print("%s -> %s"%(old_name,new_name))
    print(len(s),len(s_old))
    used_list.append(new_name)

    name = old_name.strip(".wav") + "@" + new_name
    if s.shape[0] > s_old.shape[0]:
        s_old = np.pad(s_old,(0,s.shape[0]-s_old.shape[0]),mode="constant")
    else:
        s_old = s_old[:s.shape[0]]
    
    print(len(s),len(s_old))
    
    #compute the active speech level 
    [Px,asl,c0] = asl_P56(s,float(fs),float(16))
    #`Px` is the active speech level ms energy, asl is the active factor, and c0 is the active speech level threshold


    #randomly select a segment of the noise file
    rand_start = np.random.randint(0,v.shape[0]-s.shape[0])
    v = v[rand_start:rand_start+s.shape[0]] #ensure the random segment is the same length as the speech segment
    
    #Pn is the noise level ms energy (???)
    Pn=  (v.conj().transpose() @ v)/ len(s);
    
    # we scale the noise segment to obtain the desired SNR
    scale= np.sqrt( Px/Pn/ (10** (int(snr)/ 10)))
    #print("SNR %s -> SCALE %s"%(snr,scale))
    v = v*scale


    
    y = s + v

    
    #check that the simulated signal is valid
    # NOTE: You can remove this to speed up the simulation
    try:
        #resample to 16kHz such that the PESQ score can be computed
        s_16 = resample(s,fs,16000)
        y_16 = resample(y,fs,16000)
        pesq_score = pysepm.pesq(s_16,y_16,16000)[1]
        print("PESQ: ",pesq_score)
    except:
        #try again this time with a different welsh file
        
        print("retrying")
        print("-----------------")
        used_list = simulate(s_name,v_name,snr,used_list)
    sf.write("%s/train/%s"%(OUTPUT_ROOT,name),y,fs)
    sf.write("%s/train_clean/%s"%(OUTPUT_ROOT,name),s,fs)
    
    #write the rerecorded audio to a file
    
    return used_list # return the entry to be written to the json file

if __name__=='__main__':
    out_dict = {}
    
    cafeteria,fs = sf.read("%s/PCAFETER/ch01.wav"%DEMAND_ROOT)
    car,fs = sf.read("%s/TCAR/ch01.wav"%DEMAND_ROOT)
    kitchen,fs = sf.read("%s/DKITCHEN/ch01.wav"%DEMAND_ROOT)
    meeeting,fs = sf.read("%s/OMEETING/ch01.wav"%DEMAND_ROOT)
    metro,fs = sf.read("%s/TMETRO/ch01.wav"%DEMAND_ROOT)
    restaurant,fs = sf.read("%s/PRESTO/ch01.wav"%DEMAND_ROOT)
    ssn,fs = sf.read("%s/ssn.wav"%DEMAND_ROOT)
    station,fs = sf.read("%s/PSTATION/ch01.wav"%DEMAND_ROOT)
    traffic,fs = sf.read("%s/STRAFFIC/ch01.wav"%DEMAND_ROOT)
    babble,fs = sf.read("%s/babble.wav"%DEMAND_ROOT)
    
    #don't use the same files as the test set
    used_list = os.listdir("%s/test_clean/"%OUTPUT_ROOT)
    #used_list = [x.strip(".wav") for x in used_list]
    print("USED IN TESTSET:\n",used_list)
    with open("log_trainset_28spk.csv") as f:
        reader = csv.reader(f)  # read the csv file
        # for each row, call simulate()
        next(reader,None) # skip the header row

        for i,row in enumerate(reader):
            name,loc,snr = row
            print(i,name,loc,snr)
            s_path = "%s/clean_trainset_28spk_wav/%s.wav"%(VOICEBANK_ROOT,name)
        
            print("loc is ",loc)
            if loc == "babble":
                v_path = babble
            elif loc == "cafeteria":
                v_path = cafeteria
            elif loc == "car":
                v_path = car
            elif loc == "kitchen":
                v_path = kitchen
            elif loc == "meeting":
                v_path = meeeting
            elif loc == "metro":
                v_path = metro
            elif loc == "restaurant":
                v_path = restaurant
            elif loc == "ssn":
                v_path = ssn
            elif loc == "station":
                v_path = station
            elif loc == "traffic":
                v_path = traffic
            else:
                print("Error: location not found")
            used_list = simulate(s_path,v_path,snr,used_list)
            #print("----------------------------------------------------")
            #input("Press Enter to continue...")
            
    f.close()
            