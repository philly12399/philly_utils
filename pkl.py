import pickle
# a="/home/philly12399/philly_data/kitti/kitti_dbinfos_train.pkl"
# with open(a, 'rb') as file:
#     data = pickle.load(file)
#     print(data['Car'][:10])

    
import numpy as np

def read_gt_points_from_bin(bin_file):
    gt_points = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)
    return gt_points

# 示例用法
import os
p = "/home/philly12399/philly_data/kitti/gt_database/"
p="./output/"
for b in os.listdir(p)[:10]:
    print(b)
    gt_points = read_gt_points_from_bin(p+b)
    print(gt_points.shape)