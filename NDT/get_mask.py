import os 
import pickle
import open3d as o3d
import numpy as np
import plot 
import math
def get_mask(pcd, box, mask_ratio=0.6):
    # 旋轉到和xy對齊
    R = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_xyz((0, 0,box['roty'])) 
    R_inv = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_xyz((0, 0,-box['roty']))
    pcd = np.dot(R_inv, pcd.T).T
    
    # 對長軸鏡射，使pcd左右方都有
    if(box['l'] > box['w']):
        Reflect = np.array([[1,0,0],[0,-1,0],[0,0, 1]])
    else :
        Reflect = np.array([[-1,0,0],[0,1,0],[0,0, 1]])
    pcdR = np.dot(Reflect, pcd.T).T
    pcd = np.concatenate((pcd, pcdR), axis=0)
    # voxelize
    # voxel,empty_voxel = voxelize(pcd, box)
    
    p= o3d.geometry.PointCloud()
    p.points = o3d.utility.Vector3dVector(pcd)
    vis = o3d.visualization.Visualizer()
    
    vis.create_window()
    drawbox(vis,box)
    vis.add_geometry(p)
    # for e in empty_voxel:
    #     drawbox(vis,e)
    vis.get_render_option().background_color = np.asarray([0, 0, 0]) # 設置一些渲染屬性
    vis.run()
    vis.destroy_window()
    
    

def drawbox(vis,box):
    b = o3d.geometry.OrientedBoundingBox()
    b.center = [box['x'],box['y'],box['z']]
    b.extent = [box['l'],box['w'],box['h']]
    vis.add_geometry(b)
    
def voxelize(pcd, box, voxel_size=0.3):
    l, w, h = box['l'], box['w'], box['h']
    # ln,wn,hn = int(l/voxel_size),int(w/voxel_size),int(h/voxel_size)
    ln,wn,hn = math.ceil(l/voxel_size),math.ceil(w/voxel_size),math.ceil(h/voxel_size)
    voxel = []    
    for i in range(0, ln):
        for j in range(0, wn):
            for k in range(0, hn):
                voxel.append({
                    'x': i * voxel_size - l/2 + voxel_size/2 ,
                    'y': j * voxel_size - w/2 + voxel_size/2 ,
                    'z': k * voxel_size - h/2 + voxel_size/2 ,
                    'l': voxel_size,
                    'w': voxel_size,
                    'h': voxel_size,
                    'cnt':0
                })
    pmax = pcd.max(0)-voxel_size/2
    pmin = pcd.min(0)+voxel_size/2
    for p in pcd:
        i,j,k = int((p[0]+l/2)/voxel_size), int((p[1]+w/2)/voxel_size), int((p[2]+h/2)/voxel_size)
        idx = i*wn*hn+j*hn+k            
        voxel[idx]['cnt']+=1
    empty=[]
    for v in voxel:
        if(v['cnt'] == 0):
            if(in_range(np.array([v['x'],v['y'],v['z']]), pmax, pmin)):
                empty.append(v)
    return voxel,empty

def in_range(v, pmax, pmin):
    return (v<=pmax).all() and (v>=pmin).all()

if __name__ == "__main__":
    data_root = '/home/philly12399/thesis/philly_utils/point_mae/input/seq4_car_occ0'
    pcd_path = os.path.join(data_root, 'shapenet_pc')
    info_path = os.path.join(data_root, 'ShapeNet-55')
    with open(os.path.join(info_path, f'test.txt'), 'r') as f:
        data_list_file = f.readlines()
        
    with open(os.path.join(info_path, f'test.pkl'), 'rb') as f:
        data_info = pickle.load(f)['0004']
        
    for i, d in enumerate(data_list_file):
        if(i>2):
            break
        d = d.strip()
        bin_file = os.path.join(pcd_path, d)
        pcd = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)[:,:3]
        box = data_info[i]['obj']['box3d']
        box['x'],box['y'],box['z'] = 0,0,0
        get_mask(pcd, box)
