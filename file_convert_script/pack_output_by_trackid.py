import open3d as o3d
import os 
import numpy as np
import click
import sys
import pickle
from tqdm import tqdm
CLASS='test'

@click.command()
### Add your options herea
@click.option(
    "--pcd_path",
    "-p",
    type=str,
    default=f"/home/philly12399/thesis/philly_utils/point_mae/output/{CLASS}_rand_0.9_occall/",
    help='mae vis output directory',
)

@click.option(
    "--info_path",
    "-i",
    type=str,
    default=f"/home/philly12399/thesis/philly_utils/point_mae/input/seq4_{CLASS}_all/ShapeNet-55/test.pkl",
    help='path of info pkl',
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default=f"./output_bytrackid/{CLASS}_all/",
    help='path of output',
)

def pack_output_by_trackid(pcd_path, info_path, outpath):
    pcd_path = os.path.join(pcd_path, 'vis')

    clsmap = {'car':"02958343", 'cyclist':"03790512", 'truck':"02924116"}

    with open(info_path, 'rb') as file:
        datainfo = pickle.load(file)
    allinfo = []
    for seq in datainfo:
        allinfo += datainfo[seq]
    tracks={} 
    tracks_info={}
    ##collect each info by trackid
    for i,info in enumerate(tqdm(allinfo)):
        obj = info['obj']
        clsid = clsmap[obj['obj_type']]
        tid = str(obj['track_id']).zfill(6)
        d = os.path.join(pcd_path, f"{clsid}_{i}")
        if(not os.path.isdir(d)):
            break
        if(tid not in tracks):
            tracks[tid] = []
            tracks_info[tid] = []
        tracks[tid].append(d)
        tracks_info[tid].append(info)
        
    split =['mask.txt','dense_points.txt','gt.txt']
    os.system(f'mkdir -p {outpath}')
    for _ , tid in enumerate(tqdm(tracks)):
        dir1 = os.path.join(outpath, tid)
        os.system(f'mkdir -p {dir1}')
        for i, frame in enumerate(tracks[tid]):
            for s in range(len(split)):
                f1 = os.path.join(frame, f"{split[s]}")
                f2 = os.path.join(dir1, f"{str(i).zfill(6)}_{split[s]}")
                os.system(f'cp {f1} {f2}')
    with open(os.path.join(outpath, "info.pkl"), 'wb') as file:
        pickle.dump(tracks_info, file)

    
   

if __name__ == "__main__":
    pack_output_by_trackid()
    

    