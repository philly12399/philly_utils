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
def gtdb_vis(root,seq,num=-1):
    gtdb=os.path.join(root,"gt_database/")
    pkl_path=os.path.join(root,"info.pkl")
    pkl=io_utils.read_pkl(pkl_path)
    seq = str(seq).zfill(4)
    mode='path'
    
    for i,x in enumerate(pkl[seq]):
        if(num!=-1 and i>=num): break
        pcd_file=os.path.join(gtdb,seq,x[mode])
        # print(dense_file)        
        print(x)
        pcd=io_utils.read_gt_points_from_bin(pcd_file)
        bbox=x['obj']['box3d']
        bbox['x'],bbox['y'],bbox['z']=0,0,0 
        print(bbox['roty'])
        plot.draw_pcd_and_bbox_v2(pcd,bbox)
        
def dense_vis(root,seq,num=-1):
    gtdb=os.path.join(root,"gt_database/")
    pkl_path=os.path.join(root,"info.pkl")
    pkl=io_utils.read_pkl(pkl_path)
    seq = str(seq).zfill(4)
    mode='mae_dense_path'
    for i,x in enumerate(pkl[seq]):
        if(num!=-1 and i>=num): break        
        dense_file=os.path.join(gtdb,x[mode])
        # print(dense_file)     
        print(x)   
        dense=io_utils.read_gt_points_from_bin(dense_file)
        bbox=x['obj']['box3d']
        bbox['x'],bbox['y'],bbox['z'],bbox['roty']=0,0,0,0
        plot.draw_pcd_and_bbox_v2(dense,bbox)     
        
if __name__ == '__main__':
    # root="/home/philly12399/philly_utils/data/point_mae/exp0530/"
    root="/home/philly12399/philly_utils/data/point_mae/gt_db/kitti/diff0_gtdb/"
    gtdb_vis(root,1,-1)
    # root="/home/philly12399/thesis/Point-MAE/dense_128_testing"    
    # dense_vis(root,0,5)