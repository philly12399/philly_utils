import pickle
import os
import pdb
def read_pkl(path): 
    # path="/home/philly12399/thesis/philly_utils/output/kitti_dbinfos_train.pkl"
    with open(path, 'rb') as file:
        data = pickle.load(file)
        # print(data['Car'][:10])
        # print(data[0])
        return data
def merge_pkl(a,b,out):
    info_a=read_pkl(a)
    info_b=read_pkl(b)
    for c in info_b:
        if c not in info_a:
            info_a[c]=info_b[c]
    with open(out, 'wb') as file:
        pickle.dump(info, file)
if __name__=="__main__":
    root="/home/philly12399/philly_data/point_mae/gt_db/kitti/diff0_gtdb/"
    info=os.path.join(root,"info.pkl")
    info21=os.path.join(root,"info21.pkl")
    info_merge=os.path.join(root, "info_merged.pkl")
    m=read_pkl(info_merge)
    for c in m:
        print(c,len(m[c]))
    # merge_pkl(info,info21,info_merge)
    
