CV_ROOT=$1
NUM_CANDIDATES=$2
echo "Finding $2 candidates"
echo "This will copy and reformat the selected files - make sure you have enough space!"
echo "This may take a while, please be patient"

python3 -W ignore get_candidates.py $CV_ROOT $NUM_CANDIDATES
echo "Finding durations"
python3 get_duration.py $CV_ROOT
echo "Done!"