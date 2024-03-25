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
    voxel = voxelize(box)
    
    # visualize
    p = o3d.geometry.PointCloud()
    p.points = o3d.utility.Vector3dVector(pcd)
    
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(p)
    drawbox(vis,box)
    vis.get_render_option().background_color = np.asarray([0, 0, 0]) # 設置一些渲染屬性
    vis.run()
    vis.destroy_window() 
    return

def drawbox(vis,box):
    b = o3d.geometry.OrientedBoundingBox()
    b.center = [box['x'],box['y'],box['z']]
    b.extent = [box['l'],box['w'],box['h']]
    vis.add_geometry(b)
    
def voxelize(box, voxel_size=0.3):
    l, w, h = box['l'], box['w'], box['h']
    voxel = []    
    for x in range(0, int(l/voxel_size)):
        for y in range(0, int(w/voxel_size)):
            for z in range(0, int(h/voxel_size)):
                voxel.append({
                    'x': x * voxel_size - l/2,
                    'y': y * voxel_size - w/2,
                    'z': z * voxel_size - h/2,
                    'l': voxel_size,
                    'w': voxel_size,
                    'h': voxel_size
                })
    return voxel

if __name__ == "__main__":
    data_root = '/home/philly12399/philly_utils/output/seq4_car_occ0/'
    pcd_path = os.path.join(data_root, 'shapenet_pc')
    info_path = os.path.join(data_root, 'ShapeNet-55')
    with open(os.path.join(info_path, f'test.txt'), 'r') as f:
        data_list_file = f.readlines()
        
    with open(os.path.join(info_path, f'test.pkl'), 'rb') as f:
        data_info = pickle.load(f)['0004']
        
    for i, d in enumerate(data_list_file):
        if(i>1):
            break
        d = d.strip()
        bin_file = os.path.join(pcd_path, d)
        pcd = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)[:,:3]
        box = data_info[i]['obj']['box3d']
        box['x'],box['y'],box['z'] = 0,0,0
        get_mask(pcd, box)