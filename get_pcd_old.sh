#!/usr/bin/env bash
set -e
function print_usage() {
    echo "example usage: $0 datapath expname"
}

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$script_dir"
DATA_PATH=$1
shift || {
    print_usage
    exit 1
}
MANIFEST_FILE=/home/philly12399/LCTK/rust-bin/pcd-tool/Cargo.toml
EXP_NAME="$1"
EXP_NAME="${EXP_NAME:-"newdata"}"
SAVE_PATH=$script_dir/hb_test/$EXP_NAME
rm $SAVE_PATH -rf
mkdir -p $SAVE_PATH
for d in $DATA_PATH/*; do
    echo $d
    name=$(basename $d)  
    mkdir -p "$SAVE_PATH/$name"
    ! cargo run --release \
          --manifest-path "$MANIFEST_FILE" \
          -- \
          convert \
          "$d/lidar.pcap" \
          "$SAVE_PATH/$name/" \
          10 \
          5
    python3  pcd2bin.py  convert "$SAVE_PATH/$name/" "$SAVE_PATH/${name}_bin" 999
    rm -rf $SAVE_PATH/$name/
done