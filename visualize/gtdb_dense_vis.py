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

if __name__ == '__main__':
    root="/home/philly12399/philly_utils/data/point_mae/exp0530/"
    exp="kt_dense_64"
    dense_path=os.path.join(root,exp)
    gtdb=os.path.join(dense_path,"gt_database/")
    pkl_path=os.path.join(dense_path,"info.pkl")
    pkl=io_utils.read_pkl(pkl_path)
    seq='0000'
    # pdb.set_trace()

    for x in pkl[seq]:
        dense_file=os.path.join(gtdb,x['mae_dense_path'])
        print(dense_file)
        dense=io_utils.read_gt_points_from_bin(dense_file)
        bbox=x['obj']['box3d']
        bbox['x'],bbox['y'],bbox['z'],bbox['roty']=0,0,0,0
        plot.draw_pcd_and_bbox_v2(dense,bbox)
        # pdb.set_trace()
        
    
       
    # print(pkl.keys())
    pdb.set_trace()