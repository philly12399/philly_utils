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
        # one track only
        break
    
    VOXEL_SIZE = 1.0
    DENSITY = 1000
    NUM_SAMPLES = int((VOXEL_SIZE**3)*DENSITY)
    PDF_FLAG=True
    if(PDF_FLAG):
        print(f"Sample {NUM_SAMPLES} points per voxel")
    
    for i, tid in enumerate(track):
        t_info = info[tid]
        frames = track[tid]
        l=[]  
        allpts=[]
        for fi, f in enumerate(frames):
            pcd = read_vis_points(f)
            vis.create_window()
            bbox = t_info[fi]['obj']['box3d']
            bbox['x'],bbox['y'],bbox['z'] = 0,0,0
            
            voxel = voxelize(pcd,bbox,VOXEL_SIZE,overlap=True)

            
            # # drawbox(vis,bbox,color = [1,0,0])
            p_mean = []
            pts = []
            pdf = []

            for v in voxel:
                # drawbox(vis,v)
                if(len(v["pts"]) > 0):
                    pts += v["pts"].tolist()
                if(v['mean'] is not None):
                    p_mean.append(v['mean'])  
                    #random sample     
                    if(PDF_FLAG):                                    
                        samples = np.random.multivariate_normal(v['mean'], v['cov'], NUM_SAMPLES)
                        pdf.append(samples.tolist())

            allpts+=p_mean 
            if(PDF_FLAG):                      
                pdf = np.array(pdf).reshape(-1,3) 
                print(pdf.shape)
            # p = o3d.geometry.PointCloud()
            # p.points = o3d.utility.Vector3dVector(p_mean)
            # p.points = o3d.utility.Vector3dVector(np.array(pts))
            # p.points = o3d.utility.Vector3dVector( pdf )
            
            # vis.add_geometry(p)
            # vis.get_render_option().background_color = np.asarray([0, 0, 0])
            # vis.run()
            # vis.destroy_window()
        # print(len(allpts))
        # exit()
        
        vis.create_window()
        p = o3d.geometry.PointCloud()
        p.points = o3d.utility.Vector3dVector(allpts)
        vis.add_geometry(p)
        vis.run()
        vis.destroy_window()

        
    # pdb.set_trace()
    # exit()

def voxelize(pcd, box, voxel_size=0.3, overlap=True):
    l, w, h = box['l'], box['w'], box['h']
    voxel = []    
    origin = 0
    # origin = voxel_size/2
    if(overlap):
        stride = voxel_size/2
        neighbor = [-1,0,1]
        scalar=8
    else:
        stride = voxel_size
        neighbor = [0]
        scalar=1
        
    ln, wn, hn = math.ceil(l / (stride))+1, math.ceil(w / (stride))+1, math.ceil(h / (stride))+1
    voxel = []
    for i in range(0, ln):
        for j in range(0, wn):
            for k in range(0, hn):
                # 起點voxel中心在原點,如果想讓左下在原點就要+voxel_size/2,並把ln,wn,hn -1
                voxel.append({
                    'x': i * (stride) - l / 2 + origin,
                    'y': j * (stride) - w / 2 + origin,
                    'z': k * (stride) - h / 2 + origin,
                    'l': voxel_size,
                    'w': voxel_size,
                    'h': voxel_size,
                    'pts': []
                })
   
    #regular
    incnt = 0
    for p in pcd:
        i,j,k = int((p[0]+l/2+ (voxel_size/2-origin))/(stride)), int((p[1]+w/2+ (voxel_size/2-origin))/(stride)), int((p[2]+h/2+ (voxel_size/2-origin))/(stride))   
        for di in neighbor:
            for dj in neighbor:
                for dk in neighbor:                        
                    idx = (i+di)*wn*hn + (j+dj)*hn + (k+dk)
                    if(idx >= 0 and idx < len(voxel)):
                        if(in_bbox(p,voxel[idx])):                                
                            voxel[idx]['pts'].append(p)
                            incnt += 1  
                           
    assert incnt == scalar*len(pcd)
    # #statistic
    for vi,v in enumerate(voxel):     
        v["pts"] = np.array(v["pts"])          
        if(len(v["pts"]) > 1):
            v['mean'] = np.mean(v["pts"],0)
            v['var'] =  np.var(v["pts"],0)
            v['cov'] = np.cov(v["pts"],rowvar=False)
            v['cov_inv'] = np.linalg.pinv(v['cov'])             
        else:
            v['mean'] = None
            v['var'] =  None
            v['cov'] = None
            v['cov_inv'] = None
    return voxel


               
def read_vis_points(pcd_path):
    arr=[]
    with open(pcd_path, 'r') as file:
        data = file.readlines()
        for d in data:
            d = d.replace('\n','').split(';')
            arr.append([float(d[0]), float(d[1]), float(d[2])])    
    arr = np.array(arr)
    #unique
    arr = np.unique(arr,axis=0)
    return arr


    
def drawbox(vis,box,pts=False,color=[0,0,0]):
    b = o3d.geometry.OrientedBoundingBox()
    b.center = [box['x'],box['y'],box['z']]
    b.extent = [box['l'],box['w'],box['h']]
    b.color = color
    vis.add_geometry(b)
    if(pts and len(box["pts"]) > 0 ):
        p = o3d.geometry.PointCloud()
        p.points = o3d.utility.Vector3dVector(box["pts"])
        vis.add_geometry(p)


    
def rank_list(input_list):
    ranked_list = sorted(range(len(input_list)), key=lambda x: input_list[x])
    return [ranked_list.index(i) for i in range(len(input_list))]

def in_bbox(point, bbox):
    x = point[0]
    y = point[1]
    z = point[2]
    x_min = bbox['x'] - bbox['l'] / 2
    x_max = bbox['x'] + bbox['l'] / 2
    y_min = bbox['y'] - bbox['w'] / 2
    y_max = bbox['y'] + bbox['w'] / 2
    z_min = bbox['z'] - bbox['h'] / 2
    z_max = bbox['z'] + bbox['h'] / 2
    return (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max) & (z >= z_min) & (z <= z_max)

if __name__ == '__main__':
    test()   
 
# s=torch.mean(dist1) + torch.mean(dist2)           