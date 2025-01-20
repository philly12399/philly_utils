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
    # cls=['cyclist']
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
    
def merge_NDT_of_track(tracks_obj,root_dense,EXP_PATH,max_occ=1):
    root_dense = os.path.join(root_dense,'gt_database/')
    cls=tracks_obj.keys()
    cls=['car']
    for c in cls:
        trks=tracks_obj[c]
        trackid_exp_path=os.path.join(EXP_PATH,c)
        merged_track_exp_path=os.path.join(EXP_PATH,f"{c}_all")      
        os.system(f"mkdir -p {merged_track_exp_path}")
        merged_member={}
        for trackid in trks:
            track = trks[trackid]
            print(f"merging {c} trackid:{trackid} len:{len(trks)}")
            trackid_str=str(trackid).zfill(4)
            merged_member[trackid_str]=[]            
            merged_dense_path=os.path.join(merged_track_exp_path,f"{trackid_str}.pkl")
            merged_dense = np.empty((0, 4)).astype(np.float32) 
            for i,x in enumerate(track):
                if(x['valid'] and x['obj']['occlusion']<=max_occ):
                    dense_file=os.path.join(root_dense,x['mae_dense_path'])
                    dense=io_utils.read_gt_points_from_bin(dense_file)                    
                    dense = np.hstack((dense, np.zeros((dense.shape[0], 1)))).astype(np.float32)
                    merged_dense = np.concatenate((merged_dense, dense), axis=0)     
                    merged_member[trackid_str].append(i)
            merged_dense.tofile(merged_dense_path)
            md2 = io_utils.read_gt_points_from_bin(merged_dense_path)             
        io_utils.write_pkl(merged_member,os.path.join(merged_track_exp_path,"merged_member.pkl"))            
    return

def merged_pcd_test(tracks_obj, EXP_PATH):
    cls=tracks_obj.keys()
    cls=['car']
    for c in cls:
        trks=tracks_obj[c]
        trackid_exp_path=os.path.join(EXP_PATH,c)
        merged_track_exp_path=os.path.join(EXP_PATH,f"{c}_all")      
        merged_member=io_utils.read_pkl(os.path.join(merged_track_exp_path,"merged_member.pkl"))
        for trackid in merged_member:
            print(f"track:{trackid}, merge {len(merged_member[trackid])} frames")
            track = trks[int(trackid)]
            track_member = [track[i] for i in merged_member[trackid]]
            merged_dense_path=os.path.join(merged_track_exp_path,f"{trackid}.pkl")
            merged_dense = io_utils.read_gt_points_from_bin(merged_dense_path)       
            bbox=track_member[0]['obj']['box3d']
            bbox['x'],bbox['y'],bbox['z'],bbox['roty']=0,0,0,0
            random_rows = merged_dense[np.random.choice(merged_dense.shape[0], 4096, replace=False)]
            # plot.draw_pcd_and_bbox_v2(random_rows,bbox) 
        #     for i,x in enumerate(track):
        #         if(x['valid'] and x['obj']['occlusion']<=max_occ):
        #             dense_file=os.path.join(root_dense,x['mae_dense_path'])
        #             dense=io_utils.read_gt_points_from_bin(dense_file)
        #             dense = np.hstack((dense, np.zeros((dense.shape[0], 1))))
        #             merged_dense = np.concatenate((merged_dense, dense), axis=0)                   
        #             merged_member[trackid_str].append(i)     
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
    
    # pdb.set_trace()
    # 把原本的NDT cache照trackid分類
    # get_NDT_by_trackid(tracks_obj,root_dense,NDT_cache_path,EXP_PATH)
    # merge_NDT_of_track(tracks_obj,root_dense,EXP_PATH)
    merged_pcd_test(tracks_obj,EXP_PATH)