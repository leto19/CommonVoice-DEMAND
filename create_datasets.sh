CV_ROOT=$1
VOICEBANK_ROOT=$2
DEMAND_ROOT=$3
OUTPUT_ROOT=$4





echo "Creating directories"
mkdir $OUTPUT_ROOT
mkdir $OUTPUT_ROOT/train
mkdir $OUTPUT_ROOT/train_clean
mkdir $OUTPUT_ROOT/test
mkdir $OUTPUT_ROOT/test_clean

echo "Creating Test Set"
python3 testset_create.py $CV_ROOT $VOICEBANK_ROOT $DEMAND_ROOT $OUTPUT_ROOT


echo "Creating Training Set"
echo "This may take a while, please be patient"
python3 trainset_create.py $CV_ROOT $VOICEBANK_ROOT $DEMAND_ROOT $OUTPUT_ROOT



echo "Resampling to 16kHz"
./resample.sh $OUTPUT_ROOT


echo "Creating json files"
python3 build_json_train.py $OUTPUT_ROOT $CV_ROOT $VOICEBANK_ROOT
python3 build_json_valid.py $OUTPUT_ROOT $CV_ROOT $VOICEBANK_ROOT
python3 build_json_test.py $OUTPUT_ROOT $CV_ROOT $VOICEBANK_ROOT

echo "Done!"