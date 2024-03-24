import pickle
import numpy as np
import os
import open3d as o3d
import plot
from tqdm import tqdm
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
        
def extract_class_shapenet(classname):
    classname = classname.lower()
    clsmap = {'car':"02958343", 'motorbike':"03790512", 'bus':"02924116"}
    if(not classname in clsmap):
        print(f"class {classname} not found")
        return
    cid = clsmap[classname]
    path="/home/philly12399/philly_data/ShapeNet55-34/"
    outpath = path+"/class/"+classname
    os.system(f"mkdir -p {outpath}")
    npy_path=os.path.join(path, "shapenet_pc")
    map_path=os.path.join(path, "ShapeNet-55")
    
    split = ['train','test']
    for s in split:
        buffer=""
        flist=[]
        outpath1 = os.path.join(outpath, "shapenet_pc")
        outpath2 = os.path.join(outpath, "ShapeNet-55")
        os.system(f"mkdir -p {outpath1}")
        os.system(f"mkdir -p {outpath2}")        
        with open(os.path.join(map_path, s+'.txt'), 'rb') as file:
           lines = file.readlines()
           for l in lines:
                l = l.decode('utf-8').replace('\n','')
                if(l[:8] == cid):              
                    flist.append(l)
                    buffer+=l+'\n'                    
        for f in tqdm(flist):
            a=os.path.join(npy_path, f)
            os.system(f"ln {a} {outpath1} ")
        with open(os.path.join(outpath2, f'{s}.txt'), 'w') as file:
            file.write(buffer)
            
def pack_data(binpath,outpath,cls='car'):
    l = sorted(os.listdir(binpath))
    outpath1 = os.path.join(outpath, "shapenet_pc")
    outpath2 = os.path.join(outpath, "ShapeNet-55")
    os.system(f"mkdir -p {outpath1}")
    os.system(f"mkdir -p {outpath2}")
    
    clsmap = {'car':"02958343", 'motorbike':"03790512", 'bus':"02924116"}
    c = clsmap[cls]
    buffer=""
    for f in l:
        buffer += f"{c}-{f}\n"
        a = os.path.join(binpath,f)
        b= os.path.join(outpath1,f"{c}-{f}")
        os.system(f"cp {a} {b}")
    with open(os.path.join(outpath2, f'test.txt'), 'w') as file:
        file.write(buffer)

if __name__ == "__main__":
    # shapenet2pcd()
    #extract_class_shapenet('motorbike')
#    pack_data('./output/car_occ_0/gt_database/0004/','./output/shape_car_0/','car')