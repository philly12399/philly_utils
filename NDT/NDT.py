import os
import sys
import unittest
import pdb
import pickle
import numpy as np
import open3d as o3d 
import math

from NDTPDF import PDF

def test(track_root='./output_bytrackid/car_mark_all_rotxy'):
    np.random.seed(0)
    track_path = {}
    dirlist=sorted(os.listdir(track_root))
    for i in range(len(dirlist)):
        path1 = os.path.join(track_root, dirlist[i])
        if(not os.path.isdir(path1)):
            pkl=dirlist.pop(i) 
    with open(os.path.join(track_root, pkl), 'rb') as file:
        info = pickle.load(file)
    vis = o3d.visualization.Visualizer()
    # vis.get_render_option().background_color = np.asarray([0, 0, 0])
    
    for t in dirlist:
        track_path[t] = []
        tpath = os.path.join(track_root, t)
        frame_num = (int(sorted(os.listdir(tpath))[-1][:6])+1)  
        for f in range(frame_num):            
            pcd_path=os.path.join(tpath, str(f).zfill(6)+'_dense_points.txt')
            track_path[t].append(pcd_path)
        # one track only
        break
    
    VOXEL_SIZE = 0.5
    DENSITY = 100
    NUM_SAMPLES = int((VOXEL_SIZE**3)*DENSITY)
    PDF_FLAG=False    
    MIN_PTS_VOXEL = 5
    track_buffer = {}
    voxel_of_track = {}
    rep = [7,19,30,29,20,39]
    
    for ti, tid in enumerate(track_path):

        t_info = info[tid]
        frames = track_path[tid]
        track_buffer[tid] = []
        l=[]  
        allpts=[]
        for fi, f in enumerate(frames):
            pcd = read_vis_points(f)
            bbox = t_info[fi]['obj']['box3d']
            valid_voxel, invalid_voxel, voxel = voxelize(pcd, bbox, VOXEL_SIZE, overlap=True, min_pts = MIN_PTS_VOXEL)
            track_buffer[tid].append({'voxel':valid_voxel,'bbox':bbox})
            vis.create_window()
            # drawbox(vis,bbox,color = [1,0,0])
            p_mean = []
            pts = []
            pdf = []

            for vi,v in enumerate(valid_voxel):
                # drawbox(vis,v)
                p_mean.append(v['mean'])  
                # random sample     
                # if(PDF_FLAG):
                #     samples = np.random.multivariate_normal(v['mean'], v['cov'], NUM_SAMPLES)
                #     pdf.append(samples.tolist())       
                #     mvn = scipy.stats.multivariate_normal(mean=v['mean'], cov=v['cov'], allow_singular=True)
                #     mvn_sample = mvn.pdf(samples)
                #     neg_log_psi = -np.average(np.log(mvn_sample))
                #     ndt_score = -np.average(mvn_sample)                          
            allpts+=p_mean 
            # if(PDF_FLAG):                      
            #     pdf = np.array(pdf).reshape(-1,3) 
            #     print(f"Sample {NUM_SAMPLES} points per voxel. {len(valid_voxel)}/{len(invalid_voxel) + len(valid_voxel)} voxels are valid.")
            #     print(pdf.shape)
            #     print(f"NDT score: {global_ndt_score}, Neg log psi: {global_neg_log_psi}")
        # print(len(allpts))
        # p = o3d.geometry.PointCloud()            
        # p.points = o3d.utility.Vector3dVector(allpts)
        # vis.add_geometry(p)
        # vis.run()
        # vis.destroy_window() 
        v0,_,_ = voxelize(allpts, track_buffer[tid][rep[ti]]['bbox'], VOXEL_SIZE, overlap=True, min_pts = MIN_PTS_VOXEL)
        voxel_of_track[tid] = v0
    
    
    
    
    
    # ### in same track, with mean of voxel
    # for ti, tid in enumerate(track_path):   
    #     buf = track_buffer[tid] 
    #     s=[]
    #     for fi,f in enumerate(buf):
    #         score = NDT_score(f,{'voxel':v0,'bbox':buf[rep[ti]]['bbox']})
    #         s.append(score)
    #     print(s)
    #     pdb.set_trace()
    #     # trackbuf.append(track_buffer[tid][rep[ti]])
    # exit()
    # ###different track 
    # s=[]
    # for fi in range(len(trackbuf)): 
    #     for fj in range(len(trackbuf)): 
    #         score = NDT_score(trackbuf[fi],trackbuf[fj])
    #         s.append(score)  
    # s = np.array(s).reshape(len(trackbuf),len(trackbuf))
    # for si in range(len(s)):
    #     print(s[si])
    #     print(rank_list(s[si]))
    # pdb.set_trace()
    # exit()
    
    ###in same track
    for ti, tid in enumerate(track_path):
        buf = track_buffer[tid]
        ref = buf[7]
        s=[]
        for fi in range(len(buf)): 
            for fj in range(len(buf)): 
                # print(fi,fj)        
                score = NDT_score(buf[fi],ref)
                # print(score)
                s.append(score)  
            print(f"frame {fi}")
            print(s)
        # print(NDT_score(buf[1],buf[-1]))

        # s = np.array(s).reshape(len(buf),len(buf))
        # for si in range(len(s)):
        #     print(s[si])
        #     print(rank_list(s[si]))
        
        pdb.set_trace()
        break
        

def voxelize(pcd, box, voxel_size=0.3, overlap=True, min_pts = 1):
    box['x'],box['y'],box['z'] = 0,0,0
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
              
    pcd = [p for p in pcd if in_bbox(p,box)]

    #regular
    incnt=0
    for p in pcd:
        i,j,k = int((p[0]+l/2+ (voxel_size/2-origin))/(stride)), int((p[1]+w/2+ (voxel_size/2-origin))/(stride)), int((p[2]+h/2+ (voxel_size/2-origin))/(stride))   
        for di in neighbor:
            for dj in neighbor:
                for dk in neighbor:                        
                    idx = (i+di)*wn*hn + (j+dj)*hn + (k+dk)
                    if(idx >= 0 and idx < len(voxel)):
                        if(in_bbox(p,voxel[idx])):                                
                            voxel[idx]['pts'].append(p)
                            incnt+=1
    assert scalar*len(pcd) ==  incnt

        
    # #statistic
    valid_voxel = []
    invalid_voxel = []
    for vi,v in enumerate(voxel):     
        v["pts"] = np.array(v["pts"])          
        if(len(v["pts"]) > min_pts):
            #防止矩陣退化成singular，如果解出來是complex就invalid
            cov = adjust_covariance_eigenvalues(np.cov(v["pts"],rowvar=False))      
            if(np.iscomplexobj(cov)):
                invalid_voxel.append(v)
                continue
            
            v['mean'] = np.mean(v["pts"],0)
            v['cov'] = cov
            # v['cov_inv'] = np.linalg.pinv(v['cov']) 
            v['NDTpdf'] = PDF(v['mean'], v['cov'], voxel_size)
            # v['pdf'] = scipy.stats.multivariate_normal(mean=v['mean'], cov=v['cov'], allow_singular=True).pdf
            valid_voxel.append(v)
        else:
            invalid_voxel.append(v)
    return valid_voxel, invalid_voxel,voxel

def NDT_score(a, b, mixed_pdf=True):
    # a['voxel']
    pairs = []
    for i in range(len(a['voxel'])):
        min_dist = float('inf')
        closest_index = None
        pa = a['voxel'][i]
        for j in range(len(b['voxel'])):
            pb = b['voxel'][j]
            dist = (pa['x']-pb['x'])**2 + (pa['y']-pb['y'])**2 + (pa['z']-pb['z'])**2
            if dist < min_dist:
                min_dist = dist
                closest_index = j  
        pairs.append((i,closest_index))
    global_ndt_score = 0
    for (i,j) in pairs:
        score = NDT_voxel_score(a['voxel'][i], b['voxel'][j], mixed_pdf)
        global_ndt_score += score
    return global_ndt_score

def NDT_voxel_score(a, b, mixed_pdf=True):
    if(mixed_pdf):
        pdf_scores = b['NDTpdf'].mixed_pdf(a['pts'])
    else:
        pdf_scores = b['NDTpdf'].pdf(a['pts'])
    ndt_score = -np.sum(pdf_scores)
    mean_scores = np.mean(pdf_scores)
    
    return ndt_score

def NDT_voxel_CE(a, b, mixed_pdf=True):
    samples = np.random.multivariate_normal(a['mean'], a['cov'], 300)
    if(mixed_pdf):
        pdf_scores = b['NDTpdf'].mixed_pdf(samples)
    else:
        pdf_scores = b['NDTpdf'].pdf(samples)
    mean_scores = np.mean(pdf_scores)
    volume = np.linalg.det(b['cov']) ** 0.5  # 這裡假設積分範圍的體積為第一個分佈的協方差矩陣的行列式的平方根
    cross_entropy = -mean_scores * volume
    return np.sum(cross_entropy)


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


    
def drawbox(vis,box,drawpts=False,color=[0,0,0]):
    b = o3d.geometry.OrientedBoundingBox()
    b.center = [box['x'],box['y'],box['z']]
    b.extent = [box['l'],box['w'],box['h']]
    b.color = color
    vis.add_geometry(b)
    if(drawpts and len(box["pts"]) > 0 ):
        p = o3d.geometry.PointCloud()
        p.points = o3d.utility.Vector3dVector(box["pts"])
        vis.add_geometry(p)


    
def rank_list(input_list): #自己在原本list是第幾小
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

def adjust_covariance_eigenvalues(covariance_matrix): #bugged
    # return covariance_matrix
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    min_eigenvalue = np.min(eigenvalues)
    max_eigenvalue = np.max(eigenvalues)
    if min_eigenvalue < 0.001 * max_eigenvalue:
        min_eigenvalue = 0.001 * max_eigenvalue
    else: 
        return covariance_matrix        
    adjusted_eigenvalues = np.diag(np.maximum(eigenvalues, min_eigenvalue))
    adjusted_covariance_matrix = np.matmul(np.matmul(eigenvectors, adjusted_eigenvalues), np.linalg.inv(eigenvectors))

    return adjusted_covariance_matrix

        
if __name__ == '__main__':
    test()   
 