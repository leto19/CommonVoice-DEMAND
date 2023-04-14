# CommonVoice-DEMAND

Code for the creation of CommonVoice-DEMAND datasets for speech enhancment training, as proposed in the paper:

## Data Required

* VoiceBank-DEMAND
  * This is most easily obtained from SpeechBrain
  * If you're reading this, you most likely already have this data
  * The log files `log_testset.csv` and `log_trainset_28spk.csv` are provided in this repo.
* DEMAND
  * This code expects all the 48kHz sample rate DEMAND audio to be organised in a directory as follows:
    `DKITCHEN/ch01.wav  OOFFICE/ch01.wav   PSTATION/ch01.wav  STRAFFIC/ch01.wav  TMETRO/ch01.wav DLIVING/ch01.wav   PCAFETER/ch01.wav  SCAFE/ch01.wav     TBUS/ch01.wav OMEETING/ch01.wav  PRESTO/ch01.wav    SPSQUARE/ch01.wav  TCAR/ch01.wav ssn.wav babble.wav`
* CommonVoice
  * This code expects the CommonVoice portion for a specific language to be extacted
    * Note that the candidate recordings are copied and reformatted in this same directory, so make sure there is enough disk space for the number of candidates.

## Usage

There are three ways to use this repo, depending on the amount of control you want to have over the process.

### Method 1 - The Easy Way

Execute the `run.sh` Bash script:

```bash
./run /path/to/CommonVoice/en /path/to/VoiceBank/ /path/to/DEMAND/ /path/to/output/ [N_CANDIDATES]
```

`N_CANDIDATES` is optional and defaults to `20000`

This is the easiest way to create a CommonVoice-DEMAND dataset, but will take a long time; if you want a little more control over the process, try Method 2.

### Method 2 - The Silghtly Less Easy Way

1. Execute the `get_candidates.sh `Bash script: `./get_candidates.sh /path/to/CommonVoice/en N_CANDIDATES
   1. This will find the given number of candidate audio files, convert them to 48kHz WAVs and place them in `clips_validated` in the given directory.
2. Execute the `create_datasets.sh` Bash Script: `./create_datasets.sh /path/to/CommonVoice/en /path/to/VoiceBank/ /path/to/DEMAND/ /path/to/output/`
   1. This will create the datasets, create 16kHz sample rate versions, then make the json files.

### Method 3 - The Hard Way

This baiscally involves directly running the python scripts provided in the repo. You should be able to figure out what the arguments to each are from the Bash scripts and the python code itself. Only use this method if you want to customize or change the processs in some way. You'll need to  manually run ` resample.sh` to get the 16kHz version of your dataset.
