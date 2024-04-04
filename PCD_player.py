import open3d as o3d
import os 
import numpy as np
import click
import sys
@click.command()
### Add your options herea
@click.option(
    "--path",
    "-p",
    type=str,
    default="./output_bytrackid/car_all/",
    help='visualize input path',
)
@click.option(
    "--index",
    "-i",
    type=int,
    default=0,
    help='index of path and screen',
)


def show_pointcloud_dir(path,index):
    split =['dense_points.txt','mask.txt']
    s0 = split[index]
    pathdir = sorted(os.listdir(path))
    for i in range(len(pathdir)):
        path1 = os.path.join(path, pathdir[i])
        if(not os.path.isdir(path1)):
            pathdir.pop(i)            
    f_idx = 0 #frame id
    t_idx = 0 #track id
    vis = o3d.visualization.VisualizerWithKeyCallback()
    dirlen = []
    for p in pathdir:
        dirlen.append(int(sorted(os.listdir(os.path.join(path, p)))[-1][:6]))
        
    def show_pointcloud(vis):
        nonlocal f_idx
        nonlocal t_idx
        nonlocal pathdir
        nonlocal s0
        p = pathdir[t_idx]
        s = f"{p}/{str(f_idx).zfill(6)}_{s0}"
        arr=[]
        fileid=f"track-{int(p)}-{f_idx}"
        print(fileid)
        with open(os.path.join(path, s), 'r') as file:
            data = file.readlines()
            for d in data:
                d = d.replace('\n','').split(';')
                arr.append([float(d[0]), float(d[1]), float(d[2])])
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(arr)

        vis.clear_geometries()
        vis.add_geometry(pcd) # fuck bug, vis.update_geometry(pcd)沒有用！
        vis.update_renderer()
        vis.poll_events()

    def fid_forward_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        f_idx += 1
        if f_idx >= dirlen[t_idx]:
            f_idx = dirlen[t_idx] - 1
            return True
        show_pointcloud(vis)
        return True

    def fid_back_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        f_idx -= 1
        if f_idx < 0:
            f_idx = 0
            return True
            
        show_pointcloud(vis)
        return True
    
    def fid_jump_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        try:
            X=dirlen[t_idx]     
            new_fid = int(input(f"Enter frame id [0,{X}): "))
        except:
            print('error')
            return True
        if new_fid < 0 or new_fid >= dirlen[t_idx]:                   
            print(f"Invalid frame id, Range: [0,{X})")
            return True
        f_idx = new_fid           
        show_pointcloud(vis)
        return True
    
    def tid_forward_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        t_idx += 1
        f_idx = 0
        if t_idx >= len(pathdir):
            t_idx = len(pathdir) - 1
            return True
            
        show_pointcloud(vis)
        return True

    def tid_back_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        t_idx -= 1
        f_idx = 0
        if t_idx < 0:
            t_idx = 0
            return True
            
        show_pointcloud(vis)
        return True
    
    def tid_jump_callback(vis):
        nonlocal f_idx
        nonlocal t_idx
        try:
            new_tid = int(input("Enter track id: "))
        except:
            print('error')
            return True
        new_tid = str(new_tid).zfill(6)
        if(new_tid not in pathdir):
            print(f"Cannot find track id {new_tid} in pathdir")
            print(f"Valid track id: {pathdir}")
            return True
        t_idx = pathdir.index(new_tid)
        f_idx = 0            
        show_pointcloud(vis)
        return True
    def help_callback(vis):
        print("W: track+1 S: track-1  A: frame-1  D: frame+1  T: jump to track  F: jump to frame  H: help  Q: quit")
        return True
    def quit_callback(vis):
        exit()
        
    vis.create_window()
    # vis.get_render_option().point_size = 2  # set points size
    vis.register_key_callback(ord('H'), help_callback)  
    vis.register_key_callback(ord('Q'), quit_callback) 
    vis.register_key_callback(ord('D'), fid_forward_callback)  
    vis.register_key_callback(ord('A'), fid_back_callback)  
    vis.register_key_callback(ord('W'), tid_forward_callback)  
    vis.register_key_callback(ord('S'), tid_back_callback)
    vis.register_key_callback(ord('F'), fid_jump_callback)
    vis.register_key_callback(ord('T'), tid_jump_callback)
    show_pointcloud(vis)
    vis.run()

if __name__ == "__main__":
    # visualize()
    show_pointcloud_dir()

    