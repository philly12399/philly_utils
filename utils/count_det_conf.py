import numpy as np
import os
import click
import json
@click.command()
@click.option(
    "--gt_path",
    "-g",
    type=str,
    default="/home/philly12399/philly_ssd/KITTI_tracking/training/merged_det/second_iou/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of track gt.",
)
def main(gt_path):
    # convert(gt_path,"0021.txt",'wayside',out_path)
    cls_cnt={}
    conf_range=[-999,0,1,2,3,4,5,6,7,8,9,10,999]
    print(conf_range)
    for s in sorted(os.listdir(gt_path)):    
        file_path = os.path.join(gt_path,s)      
        cls_cnt[s] = count_cls(file_path,conf_range)
        print(s,cls_cnt[s])

            
def count_cls(file_path,conf_range):
    cnt=[0 for i in range(12)]
    last = -1
    with open(file_path, "r") as f:
        for line in f:
            o = line.strip().split(" ")
            c=float(o[-1])
            for i in range(12):
                if c>conf_range[i] and c<=conf_range[i+1]:
                    cnt[i]+=1
                    break   
    return cnt    

if __name__ == "__main__":
    main()