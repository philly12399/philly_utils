#!/usr/bin/env bash
set -e
function print_usage() {
    echo "example usage: $0 datapath expname"
}
DATA_PATH="$1"
DATA_PATH="${DATA_PATH:-"/mnt/nfs/wayside_team/philly_data/0825ntu/"}"
EXP_NAME="$2"
EXP_NAME="${EXP_NAME:-"0825ntu"}"
SAVE_PATH=/home/philly12399/philly_data/$EXP_NAME/skitti-format/sequences/
WAYSIDENUM=wayside3
cnt=0
for d in $DATA_PATH/*; do
    
    TIMESTAMP=$(basename $d)  
    if [ "$TIMESTAMP" = "@eaDir" ]
    then 
        continue
    fi
    if [ "$TIMESTAMP" = "skitti-format" ]
    then 
        continue
    fi
    echo $d
    
    format_cnt=$(printf "%02d" "$cnt") 
    IN="$d/$WAYSIDENUM/"
    OUT="$SAVE_PATH/$format_cnt"
    rm -rf $OUT
    mkdir -p $OUT/
    # mkdir -p "$SAVE_PATH/$TIMESTAMP"
    python3 pcd2bin.py convert $IN $OUT/velodyne -1
    echo -e "FROM:$IN\nTIME:$TIMESTAMP" >> $OUT/timestamp.txt
    cp /home/philly12399/philly_utils/config/calib.txt $OUT
    touch $OUT/times.txt
    cnt=$((cnt+1))
done