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
  
if __name__=="__main__":
    dir1 = "/mydata/point_mae/gt_db/demo_dets/info.pkl"
    # dir1="/mydata/point_mae/output/demo/info.pkl"
    i1=read_pkl(dir1)['0021']
    
    pdb.set_trace()
    # info2=read_pkl(r2)
    # info1['0001'] = info2['0001']
    # out = "/home/philly12399/philly_ssd/point_mae/gt_db/kitti/diff0_gtdb/pkl/info_0821_newseq1.pkl"
    # write_pkl(info1, out)
    

    # m=read_pkl(info_merge)
    # for c in m:
    #     print(c,len(m[c]))
    # merge_pkl(info,info21,info_merge)
    

