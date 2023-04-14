
echo "Resampling to 16kHz"

echo "creating directories"
mkdir $1/train_16k
mkdir $1/train_clean_16k
mkdir $1/test_16k
mkdir $1/test_clean_16k


for f in $1/test/*.wav; do
    echo "Resampling $f"
    sox $f -r 16000 $1/test_16k/$(basename $f)
done

for f in $1/test_clean/*.wav; do
    echo "Resampling $f"
    sox $f -r 16000 $1/test_clean_16k/$(basename $f)
done

for f in $1/train/*.wav; do
    echo "Resampling $f"
    sox $f -r 16000 $1/train_16k/$(basename $f)
done

for f in $1/train_clean/*.wav; do
    echo "Resampling $f"
    sox $f -r 16000 $1/train_clean_16k/$(basename $f)
done

echo "Done"