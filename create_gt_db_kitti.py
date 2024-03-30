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
    "--mode",
    "-m",
    type=str,
    default="track",
    help="kitti format, track or detect",
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
@click.option(
    "--clean",
    "-c",
    type=bool,
    default=False,
    help="clean output or not",
)
def create_groundtruth_database(kitti_path, out_path, mode, num, draw, clean):
    if(mode == "detect"):
        create_groundtruth_database_kitti_detect(kitti_path, out_path, num, draw, clean)
    elif(mode == "track"):
        SEQ=[]
        create_groundtruth_database_kitti_track(kitti_path, out_path, num, draw, clean,seqlist=SEQ)
    else:
        print("Please input correct mode, track or detect")
    
def create_groundtruth_database_kitti_detect(kitti_path, out_path, num, draw, clean):
    print(f"Create database from kitti detect format")        
    
    if clean and os.path.exists(out_path):
        print(f"Remove {out_path} and create again")       
        os.system("rm -r {}".format(out_path))
    
    label_path = os.path.join(kitti_path, "label_2")
    velodyne_path = os.path.join(kitti_path, "velodyne")
    calib_path = os.path.join(kitti_path, "calib")
    db_path = os.path.join(out_path, "gt_database")
    os.system(f"mkdir -p {db_path}")
    
    if(num<0):
        num = len(os.listdir(label_path))
    file_list = sorted(os.listdir(label_path))
    
    data_info=[]
    for i,l in enumerate(tqdm(file_list)):
        if(i >= num):
            break
        class_cnt={}
        fid = l[:-4]
        calib = kitti_utils.get_calib_from_file(os.path.join(calib_path, fid+".txt"))
        objs = kitti_utils.get_objects_from_label(os.path.join(label_path, l), "detect")
        points =  np.fromfile(os.path.join(velodyne_path, fid+".bin"), dtype=np.float32).reshape(-1,4)
        
        for obj in objs:

            if(obj.obj_type not in class_cnt):
                class_cnt[obj.obj_type] = 0
            else:
                class_cnt[obj.obj_type] += 1
                
            file_name = f"{fid}_{obj.obj_type}_{class_cnt[obj.obj_type]}.bin"
            in_points_flag = kitti_utils.points_in_box(points[:,:3], obj.box3d)      
            points_in_box = points[in_points_flag]     
            center = np.array([obj.box3d['x'], obj.box3d['y'], obj.box3d['z']] )
            points_in_box[:, :3] -= center
            point_num = points_in_box.shape[0]            
            points_in_box.tofile(os.path.join(db_path,file_name))
            data_info.append(get_info(obj, point_num, fid, file_name,i))
            
            if(draw):
                pl=plot.Plot()
                pl.name(file_name[:-4])
                # pl.draw_bbox_dict(obj.box3d)
                pl.draw_cube(obj.box3d['corners_3d_cam']-center)
                for p in points_in_box:
                    pl.draw_point(p)           
                pl.show1()
                
    with open(os.path.join(out_path, "kitti_dbinfos_train.pkl"), 'wb') as file:
        pickle.dump(data_info, file)
    print(f"Extract {len(data_info)} object in {num} pcd and output to {os.path.join(out_path,'gt_database')}")
        
def create_groundtruth_database_kitti_track(kitti_path, out_path, num, draw, clean, seqlist=[]):
    print(f"Create database from kitti track format")     
       
    if clean and os.path.exists(out_path):
        print(f"Remove {out_path} and create again")       
        os.system("rm -r {}".format(out_path))   
        
    all_data_info={}
    if(seqlist == []):
        seqlist = sorted(os.listdir(os.path.join(kitti_path, "velodyne")))
    print(seqlist)
    
    occ_filt=[3]
    print(f"With occlusion filter {occ_filt}")       
    class_filt=['car']
    
    for s in seqlist:
        seq = str(s).zfill(4)
        label_path = os.path.join(kitti_path, "label_02",f"{seq}.txt")
        velodyne_path = os.path.join(kitti_path, "velodyne",seq)
        calib_path = os.path.join(kitti_path, "calib",f"{seq}.txt")
        db_path = os.path.join(out_path, "gt_database",seq)
        os.system(f"mkdir -p {db_path}")        
        calib = kitti_utils.get_calib_from_file(calib_path)
        file_list = sorted(os.listdir(velodyne_path))
        
        objs = kitti_utils.get_objects_from_label(label_path, "track")
        objs_frame = [[] for i in range(len(file_list))]
        for o in objs:
            objs_frame[o.frame_id].append(o)    
                    
        data_info=[] 
        for i,l in enumerate(tqdm(file_list)):
            if(num >=0 and i >= num):
                break
            class_cnt={}
            fid = l[:-4]
            points =  np.fromfile(os.path.join(velodyne_path, fid+".bin"), dtype=np.float32).reshape(-1,4)
            for obj in objs_frame[i]:
                if(not obj.obj_type in class_filt):
                    continue
                if(not obj.occlusion in occ_filt):
                    continue
                
                if(obj.obj_type not in class_cnt):
                    class_cnt[obj.obj_type] = 0
                else:
                    class_cnt[obj.obj_type] += 1
                    
                file_name = f"{fid}_{obj.obj_type}_{class_cnt[obj.obj_type]}_track_{obj.track_id}_occ_{obj.occlusion}.bin"
                in_points_flag = kitti_utils.points_in_box(points[:,:3], obj.box3d)      
                points_in_box = points[in_points_flag]     
                center = np.array([obj.box3d['x'], obj.box3d['y'], obj.box3d['z']] )
                points_in_box[:, :3] -= center
                points_in_box.tofile(os.path.join(db_path,file_name))
                point_num = points_in_box.shape[0]
                data_info.append(get_info(obj, point_num, fid, file_name,i))
                if(draw ):
                    pl=plot.Plot()
                    pl.name(file_name[:-4])
                    # pl.draw_bbox_dict(obj.box3d)
                    pl.draw_cube(obj.box3d['corners_3d_cam']-center)
                    for p in points_in_box:
                        pl.draw_point(p)           
                    pl.show1()
        print(f"Extract {len(data_info)} object in {num} pcd and output to {db_path}")
        all_data_info[seq] = data_info       
    with open(os.path.join(out_path, "kitti_dbinfos_train.pkl"), 'wb') as file:
        pickle.dump(all_data_info, file)
   
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
