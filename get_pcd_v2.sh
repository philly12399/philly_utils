#!/usr/bin/env bash
set -e
function print_usage() {
    echo "example usage: $0 datapath expname"
}
script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$script_dir"
DATA_PATH="$1"
DATA_PATH="${DATA_PATH:-"/mnt/nfs/wayside_team/2023-08-24-ntu-v2x-data/mesh-fushion/"}"
EXP_NAME="$2"
EXP_NAME="${EXP_NAME:-"newdata"}"
CLEAN=$3
CLEAN="${CLEAN:-"none"}"
MANIFEST_FILE="/home/philly12399/pcd-tool/Cargo.toml"
WAYSIDENUM=wayside3
SAVE_PATH=/home/philly12399/philly_data/$EXP_NAME
if [ $CLEAN = "clean" ]
then echo clean $SAVE_PATH
# rm $SAVE_PATH -rf
fi
# rm $SAVE_PATH -rf
mkdir -p $SAVE_PATH
# # 1 lidar
for d in $DATA_PATH/*; do
    
    TIMESTAMP=$(basename $d)  
    # echo $name
    if [ "$TIMESTAMP" = "@eaDir" ]
    then 
        continue
    fi
    echo $d
    # rm -rf "$SAVE_PATH/$TIMESTAMP/"
    mkdir -p "$SAVE_PATH/$TIMESTAMP"
    ! cargo run --release  --manifest-path "$MANIFEST_FILE" -- convert \
    -i "$d/$WAYSIDENUM/pcd/lidar1.pcap" \
    -o "$SAVE_PATH/$TIMESTAMP/$WAYSIDENUM/" \
    -t pcd.libpcl \
    --velodyne-model VLP32C \
    --velodyne-return-mode strongest \
    --start 50 --end 100
done

