# path to CommonVoice dataset for specific language
# candidate recordings will also be stored here, so make sure you have enough space
CV_ROOT=$1
# path to VoiceBank dataset (most easily obtained via speechbrain)
VOICEBANK_ROOT=$2
# path to DEMAND dataset (most easily obtained via speechbrain)
DEMAND_ROOT=$3
# path to output directory
OUTPUT_ROOT=$4
# number of candidates to generate, default 20000 (recommended)
NUM_CANDIDATES=${5:-20000}    

clear
./get_candidates.sh $CV_ROOT $NUM_CANDIDATES
./create_datasets.sh $CV_ROOT $VOICEBANK_ROOT $DEMAND_ROOT $OUTPUT_ROOT
