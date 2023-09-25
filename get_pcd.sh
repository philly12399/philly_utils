#!/usr/bin/env bash
set -e
function print_usage() {
    echo "example usage: $0 datapath expname"
}
script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$script_dir"
# DATA_PATH=$1
DATA_PATH="/mnt/nfs/wayside_team/2023-08-25-ntu-v2x-data/mesh-fushion/"
MANIFEST_FILE=/home/philly12399/LCTK/rust-bin/pcd-tool/Cargo.toml
# shift || {
#     print_usage
#     exit 1
# }
EXP_NAME="$1"
EXP_NAME="${EXP_NAME:-"newdata"}"
SAVE_PATH=$script_dir/$EXP_NAME
# rm $SAVE_PATH -rf
mkdir -p $SAVE_PATH
# 1 lidar
for d in $DATA_PATH/*; do
    echo $d
    name=$(basename $d)  
    # mkdir -p "$SAVE_PATH/$name"
    # rm -rf "$SAVE_PATH/$name/pcd"
    w=wayside3
    ! cargo run --release \
            --manifest-path "$MANIFEST_FILE" \
            -- \
            convert \
            "$d/$w/pcd/lidar1.pcap" \
            "$SAVE_PATH/$w/" \
            500 \
            10
done
# # 3 lidar
# c=1
# for d in $DATA_PATH/*; do
#     echo $d
#     name=$(basename $d)  
#     # mkdir -p "$SAVE_PATH/$name"
#     # rm -rf "$SAVE_PATH/$name/pcd"
#     for dd in $d/*; do
#         echo $dd
#         ! cargo run --release \
#             --manifest-path "$MANIFEST_FILE" \
#             -- \
#             convert \
#             "$dd/pcd/lidar1.pcap" \
#             "$SAVE_PATH/$(basename $dd)/" \
#             500 \
#             10
#         # python3  pcd2bin.py  convert "$SAVE_PATH/$name/" "$SAVE_PATH/${name}_bin" 999
#         # rm -rf $SAVE_PATH/$name/
#         c=$(($c+1))
#     done 
# done
