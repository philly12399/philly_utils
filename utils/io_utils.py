import pickle
import os
import pdb
import numpy as np
def read_pkl(path): 
    # path="/home/philly12399/thesis/philly_utils/output/kitti_dbinfos_train.pkl"
    with open(path, 'rb') as file:
        data = pickle.load(file)
        # print(data['Car'][:10])
        # print(data[0])
        return data
    
def write_pkl(data, outpath):  
    with open(outpath, 'wb') as file:
        pickle.dump(data, file)
    return

def merge_pkl(a,b,out):
    info_a=read_pkl(a)
    info_b=read_pkl(b)
    for c in info_b:
        if c not in info_a:
            info_a[c]=info_b[c]
    write_pkl(info, out)
        
def read_gt_points_from_bin(bin_file):
    gt_points = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)[:,:3]
    return gt_points     
  
# if __name__=="__main__":
    # root="/home/philly12399/philly_data/point_mae/gt_db/kitti/diff0_gtdb/"
    # info=os.path.join(root,"info.pkl")
    # info21=os.path.join(root,"info21.pkl")
    # info_merge=os.path.join(root, "info_merged.pkl")
    # m=read_pkl(info_merge)
    # for c in m:
    #     print(c,len(m[c]))
    # merge_pkl(info,info21,info_merge)
    

