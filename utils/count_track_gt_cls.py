import numpy as np
import os
import click
import json
@click.command()
@click.option(
    "--gt_path",
    "-g",
    type=str,
    default="/home/philly12399/philly_data/KITTI_tracking/training/labels/label_gt/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of track gt.",
)

def main(gt_path):
    # convert(gt_path,"0021.txt",'wayside',out_path)
    cls_cnt={}
    percentage={}
    # for s in sorted(os.listdir(gt_path)):    
    #     file_path = os.path.join(gt_path,s)      
    #     cls_cnt[s] = count_cls(file_path)
    # with open('cls.txt', 'w') as f: 
    #     for s in cls_cnt:
    #         f.write(f"{s} : {cls_cnt[s]}\n")
    cls=['car','van','truck']
    # cls=['cyclist']
    for s in sorted(os.listdir(gt_path)):    
        file_path = os.path.join(gt_path,s)      
        cls_cnt[s],percentage[s] = count_occ(file_path,cls)
    with open('cls_cnt.txt', 'w') as f: 
        f.write(f"Count occlusion on {cls}\n")
        for s in cls_cnt:
            f.write(f"{s} : {cls_cnt[s]}\n")
    with open('cls_percentage.txt', 'w') as f: 
        f.write(f"Count occlusion on {cls}\n")
        for s in cls_cnt:
            f.write(f"{s} : {percentage[s]}\n")
            
def count_cls(file_path):

    cls_cnt={'Frame':0,'Object':0,'Car':0,'Cyclist':0,'DontCare':0,'Pedestrian':0,'Truck':0,'Van':0}
    last = -1
    with open(file_path, "r") as f:
        for line in f:
            o = line.strip().split(" ")
            c=o[2]
            if(c not in cls_cnt):
                cls_cnt[c] = 0
            cls_cnt[c]+=1
            cls_cnt['Object']+=1
            last = int(o[0])
    cls_cnt['Frame'] = last+1
    return cls_cnt    

def count_occ(file_path,cls):
    cls_cnt={'Object':0}
    last = -1
    for i in range(4):
        occ= f"occ_{i}"
        cls_cnt[occ]=0
    # for i in range(3):
    #     trunc= f"trunc_{i}"
    #     cls_cnt[trunc]=0
        
    with open(file_path, "r") as f:
        for line in f:
            o = line.strip().split(" ")
            c=o[2]
            if(c.lower() not in cls):
                continue
            # trunc = f"trunc_{int(o[3])}"
            occ= f"occ_{int(o[4])}"

            # cls_cnt[trunc]+=1
            cls_cnt[occ]+=1
            cls_cnt['Object']+=1
    n=cls_cnt['Object']
    percentage={'Object':n}
    for c in cls_cnt:
        if(c!='Object'):
            if(n==0):
                percentage[c]=0.0000
            else:
                percentage[c] = round(cls_cnt[c]/n,4)
    return cls_cnt,percentage    
    
if __name__ == "__main__":
    main()