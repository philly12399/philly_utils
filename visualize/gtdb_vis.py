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
# def gtdb_vis(root,seq,num=-1):
#     gtdb=os.path.join(root,"gt_database/")
#     pkl_path=os.path.join(root,"info.pkl")
#     pkl=io_utils.read_pkl(pkl_path)
#     seq = str(seq).zfill(4)
#     mode='path'
#     print(len(pkl[seq]))
#     for i,x in enumerate(pkl[seq]):
#         if(num!=-1 and i>=num): break
#         pcd_file=os.path.join(gtdb,seq,x[mode])
#         # print(dense_file) 
#         # print(x['obj'])
#         if(x['obj']['obj_type']=='car'):    
#             print(x)
#             pcd=io_utils.read_gt_points_from_bin(pcd_file)
#             bbox=x['obj']['box3d']
#             bbox['x'],bbox['y'],bbox['z']=0,0,0 
#             plot.draw_pcd_and_bbox_v2(pcd,bbox)
        
def dense_vis(root,seq,num=-1,dense_or_gt='dense'):
    gtdb=os.path.join(root,"gt_database/")
    pkl_path=os.path.join(root,"info.pkl")
    pkl=io_utils.read_pkl(pkl_path)
    seq = str(seq).zfill(4)
    if(dense_or_gt=='dense'):
        mode='mae_dense_path'
    else:
        mode='path'
    print(len(pkl[seq]))
    for i,x in enumerate(pkl[seq]):
        if(num!=-1 and i>=num): break   
        if(dense_or_gt=='dense'):
            dense_file=os.path.join(gtdb,x[mode])
        else:
            dense_file=os.path.join(gtdb,seq,x[mode])
            
        # print(dense_file)     
        print(x)   
        # if(x['obj']['obj_type']=='car'):
        #     continue
        dense=io_utils.read_gt_points_from_bin(dense_file)
        bbox=x['obj']['box3d']
        bbox['x'],bbox['y'],bbox['z']=0,0,0
        if(dense_or_gt=='dense'):
            bbox['roty']=0
        plot.draw_pcd_and_bbox_v2(dense,bbox)     
        
if __name__ == '__main__':
    # root2="/home/philly12399/philly_ssd/point_mae/output/outputseq21/dense_128_all/info.pkl"
    # root3="/home/philly12399/philly_ssd/point_mae/output/dense_128_all/info_new.pkl"
    

    root1="/home/philly12399/philly_ssd/point_mae/output/mark_det_0/"
    # dense_vis(root1,21,dense_or_gt='gt')
    dense_vis(root1,21)

    
    
    
