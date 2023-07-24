# CommonVoice-DEMAND Dataset Creation

This repository provides the code for creating CommonVoice-DEMAND datasets for speech enhancement training as proposed in the paper. The following data is required:

## Required Data

* VoiceBank-DEMAND
  * This can be obtained easily from SpeechBrain
  * The log files `log_testset.csv` and `log_trainset_28spk.csv` are included in this repository.
* DEMAND
  * This code expects all the DEMAND audio with a sample rate of 48kHz to be organized in a directory as follows:
    `DKITCHEN/ch01.wav  OOFFICE/ch01.wav   PSTATION/ch01.wav  STRAFFIC/ch01.wav  TMETRO/ch01.wav DLIVING/ch01.wav   PCAFETER/ch01.wav  SCAFE/ch01.wav     TBUS/ch01.wav OMEETING/ch01.wav  PRESTO/ch01.wav    SPSQUARE/ch01.wav  TCAR/ch01.wav ssn.wav babble.wav`
* CommonVoice
  * This code expects the CommonVoice portion for a specific language to be extracted.
    * The candidate recordings are copied and reformatted in the same directory, so make sure there is enough disk space for the number of candidates.

## Usage

There are three methods to use this repository depending on the level of control you want to have over the process.

### Method 1 - The Easy Way

Execute the `run.sh` Bash script (in this example for the English `en` portion of CommonVoice):

```bash
./run /path/to/CommonVoice/en /path/to/VoiceBank/ /path/to/DEMAND/ /path/to/output/CommonVoice-DEMAND-EN [N_CANDIDATES]
```

Note that `N_CANDIDATES` is optional and defaults to `20000`. This is the simplest way to create a CommonVoice-DEMAND dataset, but it may take a long time. If you want more control over the process, try Method 2.

### Method 2 - The Slightly Less Easy Way

1. Execute the `get_candidates.sh `Bash script: `./get_candidates.sh /path/to/CommonVoice/en N_CANDIDATES`
   1. This script finds the given number of candidate audio files, converts them to 48kHz WAVs, and places them in `clips_validated` in the given directory.
2. Execute the `create_datasets.sh` Bash Script: `./create_datasets.sh /path/to/CommonVoice/en /path/to/VoiceBank/ /path/to/DEMAND/ /path/to/output/CommonVoice-DEMAND-EN`
   1. This script creates the datasets, creates 16kHz sample rate versions, and generates the JSON files.

### Method 3 - The Hard Way

This involves directly running the Python scripts provided in the repository. You should be able to determine the arguments to each from the Bash scripts and the Python code itself. Only use this method if you want to customize or change the process in some way. You'll need to manually run `resample.sh` to get the 16kHz version of your dataset.

## Citing this code
Please cite the following paper if you use this code in your work:

G. Close, T. Hain, and S. Goetze,
The Effect of Spoken Language on Speech Enhancement using Self-Supervised Speech Representation Loss Functions, Proc. IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), 2023

```
@InProceedings{close2023-WASPAA-Language-Effect-SSSRs-SignalEnhancement,
  author    = {George Close and Thomas Hain and Stefan Goetze},
  booktitle = {Proc.~IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA)},
  title     = {{The Effect of Spoken Language on Speech Enhancement using Self-Supervised Speech Representation Loss Functions}},
  year      = {2023},
  address   = {New Paltz, NY, USA},
  month     = oct,
}
```
