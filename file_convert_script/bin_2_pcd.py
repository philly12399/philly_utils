import os
import numpy as np
import click
from tqdm import tqdm
import open3d as o3d


@click.command()
### Add your options here
@click.option(
    "--binfolder",
    "-b",
    type=str,
    required=True,
    help="Path of input bin",
)
@click.option(
    "--pcdfolder",
    "-p",
    type=str,
    required=True,
    help="Path of output pcd",
)
@click.option(
    "--convert_number",
    "-n",
    type=int,
    default=-1,
    help="convert number",
)

def convert_click(binfolder, pcdfolder, convert_number):
    convert(binfolder, pcdfolder, convert_number)
               
def convert(binfolder, pcdfolder, convert_number):
    if(convert_number == -1):
        convert_number = 99999999
    file_list = os.listdir(binfolder)
    file_list.sort()
    count = 0
    if os.path.exists(pcdfolder):
        pass
    else:
        os.makedirs(pcdfolder)
    convert_number = min(convert_number,len(file_list))
    print("Total: ", len(file_list)," bins")
    print("Convert: ", convert_number, " bins")
    file_list = file_list[:convert_number]
    for (count,file) in  enumerate(tqdm(file_list, desc="Converting")):     
        (filename, extension) = os.path.splitext(file)
        if extension == ".bin" and count < convert_number:
            velodyne_file = os.path.join(binfolder, filename) + '.bin'
            velodyne_file_new = os.path.join(pcdfolder, filename) + '.pcd'
            bin_pcd = np.fromfile(velodyne_file, dtype=np.float32)
    
            # Reshape and drop reflection values
            points = bin_pcd.reshape((-1, 4))[:, 0:3]

            # Convert to Open3D point cloud
            o3d_pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

            # Save to whatever format you like
            o3d.io.write_point_cloud(velodyne_file_new, o3d_pcd,write_ascii=True)   

def check(binfolder, pcdfolder, convert_number):
    if(convert_number == -1):
        convert_number = 99999999
    file_list = os.listdir(binfolder)
    file_list.sort()
    count = 0
    if os.path.exists(pcdfolder):
        pass
    else:
        os.makedirs(pcdfolder)
    convert_number = min(convert_number,len(file_list))
    print("Total: ", len(file_list)," bins")
    print("Convert: ", convert_number, " bins")
    file_list = file_list[:convert_number]
    for (count,file) in  enumerate(tqdm(file_list, desc="Converting")):     
        (filename, extension) = os.path.splitext(file)
        if extension == ".bin" and count < convert_number:
            velodyne_file = os.path.join(binfolder, filename) + '.bin'
            velodyne_file_new = os.path.join(pcdfolder, filename) + '.pcd'
            bin_pcd = np.fromfile(velodyne_file, dtype=np.float32)
            print(bin_pcd.shape)
            # Reshape and drop reflection values
        


if __name__ == "__main__":
    convert_click()
