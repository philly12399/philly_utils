import open3d as o3d
import os 
import numpy as np
def convert(path='./viscar', out='./viscar_pcd'):
    # os.system(f'mkdir -p {out}')
    split = ['gt.txt', 'dense_points.txt','center.txt','vis.txt']
    num=5
    # split =['dense_points.txt','gt.txt']
    for i,f in enumerate(sorted(os.listdir(path))):
        if(num>=0 and i>=num):
            break
        path1 = os.path.join(path, f)

        for s in split:
            arr=[]
            with open(os.path.join(path1, s), 'r') as file:
                data = file.readlines()
                for d in data:
                    d = d.replace('\n','').split(';')
                    arr.append([float(d[0]), float(d[1]), float(d[2])])
            arr = np.array(arr) 
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(arr)
            o3d.visualization.draw_geometries([pcd], width=800, height=500,window_name=str(i)+'_'+s)

        
        
    # pcd = o3d.io.read_point_cloud(path + '.ply')
    # o3d.io.write_point_cloud(out + '.xyz', pcd, write_ascii=True)
    


if __name__ == "__main__":
    convert('./vis')