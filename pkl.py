import pickle
import numpy as np
import os
import open3d as o3d
import plot
def read_pkl(path): 
    # path="/home/philly12399/thesis/philly_utils/output/kitti_dbinfos_train.pkl"
    with open(path, 'rb') as file:
        data = pickle.load(file)
        # print(data['Car'][:10])
        # print(data[0])
        return data


def read_gt_points_from_bin(bin_file):
    gt_points = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)
    return gt_points

def npy2pcd(npy):
    xyz = np.load(npy)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    return pcd


def shapenet2pcd():
    classname='car'
    path="/home/philly12399/philly_data/ShapeNet55-34/class/"+classname
    outpath = "/home/philly12399/philly_data/ShapeNet55-34/class_pcd/"+classname
    os.system(f"mkdir -p {outpath}")
    idmap={}
    num = 10
    
    for i,p in enumerate(sorted(os.listdir(path))):
        if(i>=num):
            break
        print(i,p)
        pcd = npy2pcd(os.path.join(path,p))
        filename=str(i).zfill(6)+".pcd"
        idmap[filename] = p
        o3d.io.write_point_cloud(os.path.join(outpath,filename), pcd, write_ascii = True)
        
    with open(os.path.join(outpath, f'../{classname}_map.pkl'), 'wb') as file:
        pickle.dump(idmap, file)
if __name__ == "__main__":
    shapenet2pcd()