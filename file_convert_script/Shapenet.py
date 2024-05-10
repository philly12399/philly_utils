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
    gt_points = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)[:,:3]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(gt_points)
    o3d.visualization.draw_geometries([pcd,], width=800, height=500)
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
            
def pack_data_fromdb(binpath, outpath, cls='car'): #create gt db to shapenet format
    datapath=binpath[:binpath.find('gt_database')]
    
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
    os.system(f"cp {datapath}/info.pkl {outpath2}/info.pkl")
    
def pack_data_fromvis(vispath, outpath): #pointmae vis to shapenet format
    vispath = os.path.join(vispath, 'vis')
    visdir=os.listdir(vispath)
    outpath1 = os.path.join(outpath, "shapenet_pc")
    outpath2 = os.path.join(outpath, "ShapeNet-55")
    os.system(f"mkdir -p {outpath1}")
    os.system(f"mkdir -p {outpath2}")    
    cls = visdir[0][:8]
    buffer=""
    for i in range(len(visdir)):
        obj_id = f"{cls}-{i}"
        p = os.path.join(vispath, f"{cls}_{i}",'dense_points.txt')
        with open(p, 'r') as file:
            lines = file.readlines()
            xyz = []
            for l in lines:
                l = l.replace('\n','').split(';')
                xyz.append([float(l[0]), float(l[1]), float(l[2]), 0])
            xyz = np.array(xyz).astype('float32')
            xyz.tofile(os.path.join(outpath1, f"{obj_id}.bin"))
            x1=read_gt_points_from_bin(os.path.join(outpath1, f"{obj_id}.bin"))
            buffer += f"{obj_id}.bin\n"
        
    with open(os.path.join(outpath2, f'test.txt'), 'w') as file:
         file.write(buffer)
if __name__ == "__main__":
    # shapenet2pcd()
    #extract_class_shapenet('motorbike')
    # pack_data_fromdb('./output/car_occ_1/gt_database/0004/','./output/seq4_car_occ1/','car')
    cls = ['car','cyclist','truck']
    cmap = {'cyclist': 'motorbike', 'truck': 'bus'}
    # pack_data_fromdb(f'./gt_db/car_mark_all/gt_database/0004/', f'./output/seq4_car_mark_all/', 'car')
    # pack_data_fromdb(f'./gt_db/car_ab3dmot_all/gt_database/0004/', f'./output/seq4_car_ab3dmot_all/', 'car')
    
    # d=read_pkl('/home/philly12399/philly_utils/point_mae/input/seq4_car_all/ShapeNet-55/test.pkl')
    
    #Pack class-occall from db
    # for c in cls:
    #     c1 = c
    #     if c in cmap:
    #         c1 = cmap[c]
        
    #     pack_data_fromdb(f'./output/{c}_all/gt_database/0004/', f'./output/seq4_{c}_all/', c1)
    
    #Pack form mae output vis
    # for i in range(4):
    #     pack_data_fromvis(f'./point_mae/output/rand_0.9_occ{i}', f'./point_mae/vis_input/rand_0.9_occ{i}')
    
    # read_gt_points_from_bin('./point_mae/vis_input/rand_0.9_occ0/shapenet_pc/02958343-0.bin')

    

    
    
    