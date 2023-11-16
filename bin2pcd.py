import os
import numpy as np
import fire
from tqdm import tqdm
import open3d as o3d
#USAGE: python3 bin2pcd.py  convert [data] [out] [num]
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
        
        


if __name__ == "__main__":
    fire.Fire()
