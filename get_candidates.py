import pandas as pd
import os
import sys
import librosa
import sox
import os
import numpy as np
import librosa
from speech_noise import nonspeech2

CV_ROOT = sys.argv[1]
n_to_copy = int(sys.argv[2])
validated = pd.read_csv(CV_ROOT+"validated.tsv",sep="\t")
#validated = validated[validated["accents"] == "England English"]
#filter out the files that are 1 word long
validated = validated[validated["sentence"].apply(lambda x: len(x.split(" ")) > 1)] 
#fitler out the files which have more than 0 downvotes
#print(len(validated))
validated_files = validated["path"].values

if not os.path.exists(CV_ROOT+"clips_validated"):
    os.mkdir(CV_ROOT+"clips_validated")

def estimate_snr(audio_array, sr):


    # get the Non speech and speech signals
    bg,s = nonspeech2(audio_array, sr,webrtc_sr=32000)
    if len(bg) == 0:
        bg = np.zeros_like(audio_array)
    if len(s) == 0:
        s = np.zeros_like(audio_array)
    """
    plt.subplot(3,1,1)
    plt.plot(audio_array)
    plt.title("input data")
    plt.subplot(3,1,2)
    plt.plot(s)
    plt.title("all speech frames ")
    plt.subplot(3,1,3)
    plt.plot(bg)
    plt.title("all nonspeech frames")
    #plt.show()
    print("audio_array.shape",audio_array.shape)
    print("s.shape",s.shape)
    print("bg.shape",bg.shape)
    """
    #bg is all the nonspeech frames, s is all the speech frames
    bg_power = (bg ** 2).mean()
    s_power = (s ** 2).mean()
    snr = 10 * np.log10(s_power / bg_power)
    return snr

#copy the files to a new directory
i = 0
for f in validated_files:
    print(f)
    f_path = os.path.join(CV_ROOT+"clips",f)
    s,fs = librosa.load(f_path,sr=32000)
    if len(s) < 2*fs:
        print("             skipping %s"%f)

        continue
    snr_val = estimate_snr(s,fs)
    print(snr_val)
    if snr_val < 50 or np.isinf(np.abs(snr_val)):
        print("             skipping %s"%f)
        continue
    trans = sox.Transformer()
    trans.set_output_format(file_type="wav", bits=16, rate=48000)
    trans.build(f_path,os.path.join(CV_ROOT+"clips_validated",f.replace(".mp3",".wav")))
    #shutil.copyfile(f_path,os.path.join(CV_ROOT+"clips_validated_new",f))
    i += 1
    if i == n_to_copy:
        break




