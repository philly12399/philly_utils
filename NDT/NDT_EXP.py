import numpy as np
import open3d as o3d
import os
# import click
import sys
import pdb
current_dir = os.path.dirname(os.path.abspath(__file__))
# 獲取項目根目錄
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# 將項目根目錄添加到sys.path中
sys.path.append(project_root)
from utils import io_utils
from utils import plot

def get_label(file):
    lines = np.genfromtxt(file, delimiter=' ', dtype=float)
    trackid=[int(l[1]) for l in lines]
    return trackid

def get_obj_by_trackid(root,label_path,seq,vis=False):
    gtdb=os.path.join(root,"gt_database/")
    pkl_path=os.path.join(root,"info.pkl")
    pkl=io_utils.read_pkl(pkl_path)
    label_path = os.path.join(label_path,seq+'.txt')
    trackid = get_label(label_path)
    mode='mae_dense_path'
    tracks_obj = {}
    
    for i,x in enumerate(pkl[seq]):
        dense_file=os.path.join(gtdb,x[mode])            
        # print(dense_file)     
        x['obj']['track_id'] = trackid[i]
        obj_type=x['obj']['obj_type']
        x['obj']['idx'] = i
        
        if(not obj_type in tracks_obj):
            tracks_obj[obj_type] = {}
        if(not trackid[i] in tracks_obj[obj_type]):
            tracks_obj[obj_type][trackid[i]] = []
        tracks_obj[obj_type][trackid[i]].append(x)
        
        if(vis):
            dense=io_utils.read_gt_points_from_bin(dense_file)
            bbox=x['obj']['box3d']
            bbox['x'],bbox['y'],bbox['z']=0,0,0
            bbox['roty']=0
            plot.draw_pcd_and_bbox_v2(dense,bbox)     
    return tracks_obj

def write_trackid_info(tracks_obj,EXP_PATH):
    os.system(f"mkdir -p {EXP_PATH}")
    os.system(f"mkdir -p {os.path.join(EXP_PATH,'pcd')}")
    io_utils.write_pkl(tracks_obj,os.path.join(EXP_PATH,"info_by_trackid.pkl"))
    return

def get_NDT_by_trackid(tracks_obj,root_dense,NDT_cache_path,EXP_PATH):
    root_dense = os.path.join(root_dense,'gt_database/')
    cls=tracks_obj.keys()
    cls=['cyclist']
    for c in cls:
        trks=tracks_obj[c]
        trackid_exp_path=os.path.join(EXP_PATH,c)
        os.system(f"mkdir -p {trackid_exp_path}")
        cnt=0        
        for trackid in trks:
            track = trks[trackid]
            print(f"processing {c} trackid:{trackid}, {cnt}/{len(trks)}")
            for i,x in enumerate(track):
                s1=str(x['velodyne_idx']).zfill(6)
                s2=str(x['obj_det_idx']).zfill(4)
                s3=c
                old_NDT_path=os.path.join(NDT_cache_path,f"{s1}_{s2}_{s3}.pkl")
                new_NDT_path=os.path.join(trackid_exp_path,f"{str(trackid).zfill(4)}_{str(i).zfill(4)}.pkl")
                os.system(f"cp -r {old_NDT_path} {new_NDT_path}")
                # dense_file=os.path.join(root_dense,x['mae_dense_path'])
                # dense=io_utils.read_gt_points_from_bin(dense_file)
                # bbox=x['obj']['box3d']
                # bbox['x'],bbox['y'],bbox['z'],bbox['roty']=0,0,0,0
                # plot.draw_pcd_and_bbox_v2(dense,bbox)  
            cnt+=1        
            
    return
    
    
if __name__ == '__main__':
    seq=21
    seq = str(seq).zfill(4)
    
    root_gtdb="/home/philly12399/philly_ssd/point_mae/gt_db/kitti/diff0_gtdb/"   
    root_dense="/home/philly12399/philly_ssd/point_mae/output/gtdet/dense_128_all/" 
    label_path="/home/philly12399/philly_ssd/KITTI_tracking/training/label_02/"
    NDT_cache_path="/home/philly12399/philly_ssd/ab3dmot/NDT_pkl/gtdet/cache-128/"
    EXP_PATH="/home/philly12399/philly_ssd/NDT_EXP/"
    
    EXP_PATH = os.path.join(EXP_PATH,seq)  
    NDT_cache_path = os.path.join(NDT_cache_path,seq)
    os.system(f"mkdir -p {EXP_PATH}")
    overwrite=False
    INFO_PATH=os.path.join(EXP_PATH,"info_by_trackid.pkl")
    
    if(overwrite or (not os.path.exists(INFO_PATH))):
        tracks_obj = get_obj_by_trackid(root_dense,label_path,seq)
        write_trackid_info(tracks_obj,EXP_PATH)
        print("create new trackid info")
    else:
        tracks_obj = io_utils.read_pkl(INFO_PATH)
        print("load trackid info")
    
    pdb.set_trace()
    get_NDT_by_trackid(tracks_obj,root_dense,NDT_cache_path,EXP_PATH)
