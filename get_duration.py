import soundfile as sf
import sys
import csv
import os



def get_duration(filename):
    data, fs = sf.read(filename)
    #print(srmr(data,fs))
    duration = len(data) / fs
    return duration


def main():
    in_dir = sys.argv[1]
    out_file = in_dir + "clips_validated_len.csv"
    in_dir_clips = os.path.join(in_dir, "clips_validated")
    in_dir_list = os.listdir(in_dir_clips)

    out_dict = {}
    for f in in_dir_list:
        f_path = os.path.join(in_dir_clips, f)
        duration = get_duration(f_path)
        out_dict[f] = duration

    with open(out_file, 'w') as f:
        w = csv.writer(f)
        w.writerows(out_dict.items())

if __name__ == '__main__':
    main()