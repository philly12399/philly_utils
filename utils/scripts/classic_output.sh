inpath=$1
python3 clean_classic_affi.py -r $inpath
python3 collect_classic_ab3dmot_diff.py -r $inpath