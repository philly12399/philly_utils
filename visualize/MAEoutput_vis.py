import open3d as o3d
import os 
import numpy as np
import click
import sys
@click.command()
### Add your options herea
@click.option(
    "--index",
    "-i",
    type=int,
    default=0,
    help='index of path and screen',
)
@click.option(
    "--num",
    "-n",
    type=int,
    default=-1,
    help='visualize number',
)
def visualize(index,num):
    # 修改此處改變路徑
    # VIS_PATH=['./point_mae/output/car/car_rand_0.9_occall','./point_mae/output/cyclist_rand_0.9_occall']
    prefix = './tmp/mask_ratio_exp/'
    suffix = 'vis/0004'
    VIS_PATH=['vis_0.3_64','vis_0.6_64','vis_0.9_64']
    VIS_PATH[index] = os.path.join(prefix,VIS_PATH[index],suffix)
    visualize_inner(VIS_PATH[index],index,num)
    
def visualize_inner(path,index,num):
    # path = os.path.join(path, 'vis_0.3/vis/0004/')
    # os.system(f'mkdir -p {out}')
    # split = ['gt.txt', 'dense_points.txt','center.txt','vis.txt']

    # split =['mask.txt','voxelmask.txt']
    split =['dense_points.txt']
    # split=['gt.txt']
    
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
            unarr = np.unique(np.array(arr), axis=0)
            
            print(len(unarr))
            # with open(os.path.join(path1, 'mask.txt'), 'r') as file:
            #     data = file.readlines()
            #     for d in data:
            #         d = d.replace('\n','').split(';')
            #         arr.append([float(d[0]), float(d[1]), float(d[2])])
            # arr = np.array(arr)

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(arr)

            # window_name = f"{pathn}_{i}_{s}"
            window_name =  f"{f}_{s}"
            o3d.visualization.draw_geometries([pcd,], width=800, height=500,window_name=window_name,left=900*index,top=0)

        
        
    # pcd = o3d.io.read_point_cloud(path + '.ply')
    # o3d.io.write_point_cloud(out + '.xyz', pcd, write_ascii=True)
    

if __name__ == "__main__":
    visualize()
    

    