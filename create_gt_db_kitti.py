import click
import pickle
import numpy as np
import os
import kitti_utils
import plot
from tqdm import tqdm
from copy import deepcopy
# python3 create_gt_db_kitti.py
@click.command()
### Add your options here
@click.option(
    "--kitti_path",
    "-k",
    type=str,
    default="./seq4",
    help="Path of kitti",
)
@click.option(
    "--out_path",
    "-o",
    type=str,
    default="./output",
    help="Path of output",
)
@click.option(
    "--format",
    "-f",
    type=str,
    default="Philly",
    help="label format",
)
@click.option(
    "--num",
    "-n",
    type=int,
    default=-1,
    help="number of bin to convert",
)
@click.option(
    "--draw",
    "-d",
    type=bool,
    default=False,
    help="draw bbox and points",
)

def create_groundtruth_database(kitti_path, out_path, format, num, draw):
    os.system("mkdir -p {}".format(out_path))
    os.system("mkdir -p {}/gt_database".format(out_path))

    
    
    label_path = os.path.join(kitti_path, "label_2")
    velodyne_path = os.path.join(kitti_path, "velodyne")
    calib_path = os.path.join(kitti_path, "calib")
    if(num<0):
        file_list = sorted(os.listdir(label_path))
    else:
        file_list = sorted(os.listdir(label_path))[:num]
    data_info=[]
    for i,l in enumerate(tqdm(file_list)):
        class_cnt={}
        fid = l[:-4]
        calib = kitti_utils.get_calib_from_file(os.path.join(calib_path, fid+".txt"))
        objs = kitti_utils.get_objects_from_label(os.path.join(label_path, l))
        points =  np.fromfile(os.path.join(velodyne_path, fid+".bin"), dtype=np.float32).reshape(-1,4)
        
        for obj in objs:
            # if(obj.occlusion)
            
            if(obj.obj_type not in class_cnt):
                class_cnt[obj.obj_type] = 0
            else:
                class_cnt[obj.obj_type] += 1
                
            file_name = f"{fid}_{obj.obj_type}_{class_cnt[obj.obj_type]}.bin"
            in_points_flag = kitti_utils.points_in_box(points[:,:3], obj.box3d)      
            points_in_box = points[in_points_flag]     
            center = np.array([obj.box3d['x'], obj.box3d['y'], obj.box3d['z']] )
            points_in_box[:, :3] -= center
            points_in_box.tofile(os.path.join(out_path,"gt_database",file_name))
            point_num = points_in_box.shape[0]
            data_info.append(get_info(obj, point_num, fid, file_name,i))
        if(draw):
            pl=plot.Plot()
            pl.name(file_name[:-4])
            for obj in objs:
                pl.draw_bbox_dict(obj.box3d)
                # pl.draw_cube(obj.box3d['corners_3d_cam']-center)
                # for p in points_in_box:
                #     pl.draw_point(p)           
            pl.show()
    with open(os.path.join(out_path, "kitti_dbinfos_train.pkl"), 'wb') as file:
        pickle.dump(data_info, file)
        
def get_info(obj, point_num, fid, file_name,i):    
    obj1 = deepcopy(obj.__dict__)
    obj1.pop('src')    
    obj1['box3d'].pop('corners_3d_cam')
    obj1['box3d'].pop('corners_org')
    info = {'obj':obj1, 'num_points_in_gt':point_num, 'velodyne_idx':fid, 'path':file_name,'gt_idx': i}
    return(info)

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


    
if __name__ == "__main__":
    create_groundtruth_database()