import os
import sys
import unittest
import pdb
import pickle
import numpy as np
import open3d as o3d 
import math

def test(track_path='./output_bytrackid/car_mark_all_rotxy'):
    track = {}
    dirlist=sorted(os.listdir(track_path))
    for i in range(len(dirlist)):
        path1 = os.path.join(track_path, dirlist[i])
        if(not os.path.isdir(path1)):
            pkl=dirlist.pop(i) 
    with open(os.path.join(track_path, pkl), 'rb') as file:
        info = pickle.load(file)
    vis = o3d.visualization.Visualizer()
    
    for t in dirlist:
        track[t] = []
        tpath = os.path.join(track_path, t)
        frame_num = (int(sorted(os.listdir(tpath))[-1][:6])+1)  
        for f in range(frame_num):            
            pcd_path=os.path.join(tpath, str(f).zfill(6)+'_dense_points.txt')
            track[t].append(pcd_path)
        break
    
    for i, tid in enumerate(track):
        t_info = info[tid]
        frames = track[tid]
        l=[]  
        for fi, f in enumerate(frames):
            if(fi!=7):
                continue
            pcd = read_vis_points(f)
            bbox = t_info[fi]['obj']['box3d']
            bbox['x'],bbox['y'],bbox['z'] = 0,0,0
            voxel = voxelize(pcd,bbox,0.3)
            vis.create_window()
            drawbox(vis,bbox,color = [1,0,0])
            p_mean = []
            pts = []

            for v in voxel:
                # drawbox(vis,v)
                if(len(v["pts"]) > 0):
                    pts += v["pts"].tolist()
                if(v['mean'] is not None):
                    p_mean.append(v['mean'])   
            p = o3d.geometry.PointCloud()
            # p.points = o3d.utility.Vector3dVector(p_mean)
            p.points = o3d.utility.Vector3dVector(pts)
            vis.add_geometry(p)
            
            vis.get_render_option().background_color = np.asarray([0, 0, 0])
            vis.run()
            vis.destroy_window()
            break
    # pdb.set_trace()
    # exit()
    
    

    
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
                    'pts':[]
                    
                })
    pmax = pcd.max(0)-voxel_size/2
    pmin = pcd.min(0)+voxel_size/2
    for p in pcd:
        i,j,k = int((p[0]+l/2)/voxel_size), int((p[1]+w/2)/voxel_size), int((p[2]+h/2)/voxel_size)
        idx = i*wn*hn+j*hn+k            
        voxel[idx]['pts'].append(p)
    for v in voxel:
        v["pts"] = np.array(v["pts"])
        if(len(v["pts"]) >0):
            v['mean'] = np.mean(v["pts"],0)
            v['var'] =  np.var(v["pts"],0)
        else:
            v['mean'] = None
            v['var'] =  None
    return voxel

def read_vis_points(pcd_path):
    arr=[]
    with open(pcd_path, 'r') as file:
        data = file.readlines()
        for d in data:
            d = d.replace('\n','').split(';')
            arr.append([float(d[0]), float(d[1]), float(d[2])])
    
    # arr = torch.tensor(arr).reshape(1, -1, 3)   
    return np.array(arr)


    
def drawbox(vis,box,pts=False,color=[1,1,1]):
    b = o3d.geometry.OrientedBoundingBox()
    b.center = [box['x'],box['y'],box['z']]
    b.extent = [box['l'],box['w'],box['h']]
    b.color = color
    vis.add_geometry(b)
    return
    if(pts and len(box["pts"]) > 0 ):
        p = o3d.geometry.PointCloud()
        p.points = o3d.utility.Vector3dVector(box["pts"])
        vis.add_geometry(p)


    
def rank_list(input_list):
    ranked_list = sorted(range(len(input_list)), key=lambda x: input_list[x])
    return [ranked_list.index(i) for i in range(len(input_list))]

if __name__ == '__main__':
    test()   
 
# s=torch.mean(dist1) + torch.mean(dist2)           