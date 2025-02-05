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
    default="../data/KITTI_tracking/training/",
    help="Path of kitti",
)
@click.option(
    "--label",
    "-l",
    type=str,
    default="../data/KITTI_tracking/training/gt_det_set_seq/diff3",
    help="Path of label",
)
@click.option(
    "--out_path",
    "-o",
    type=str,
    default="../data/gt_db/demo",
    help="Path of output",
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
@click.option(
    "--format",
    "-f",
    type=str,
    default="kitti",
    help="dataset format kitti/wayside",
)

def create_groundtruth_database(kitti_path,label, out_path, num, draw, clean,format):
    COMBINATION="A1"
    #A1
    if(COMBINATION=="A1"):
        SEQ=[21] # wayside
        format="wayside"
    #A2
    elif(COMBINATION=="A2"):
        SEQ=list(range(0,22)) 
        format="kitti"
    #A3
    elif(COMBINATION=="A3"):
        SEQ=list(range(0,21)) 
        format="kitti"
    else: #do your own settings
        SEQ=[21] # wayside
        format="wayside"        
    create_groundtruth_database_kitti_track(kitti_path,label, out_path, num, draw, clean, seqlist=SEQ, dataset=format)

import pdb  
def create_groundtruth_database_kitti_track(kitti_path, label_path0, out_path, num, draw, clean, seqlist=[], dataset="kitti"):
    print(f"Create database from kitti track format")     
       
    if clean and os.path.exists(out_path):
        print(f"Remove {out_path} and create again")       
        os.system("rm -r {}".format(out_path))   
        
    all_data_info={}
    if(seqlist == []):
        seqlist = sorted(os.listdir(os.path.join(kitti_path, "velodyne")))
    print(seqlist)
    
    #Filter,if not in filter, drop
    CLASS_FILTER=['car','cyclist']
    OCC_FILTER=[-1,0,1,2,3] 
    MIN_POINTS=32
    MIN_POINTS_FLAG=False
    
    print(f"With occlusion filter {OCC_FILTER}, class filter {CLASS_FILTER}")       
    skipcnt=0
    for s in seqlist:
        ds=dataset
        #WARNING: hard code for wayside
        if(s>20):
            ds="wayside"
        else:
            ds="kitti"   
            
        seq = str(s).zfill(4)
        if(label_path0 != ""):
            label_path = os.path.join(label_path0, f"{seq}.txt")            
        else:
            label_path = os.path.join(kitti_path, "label_02",f"{seq}.txt")
        print(label_path)
        velodyne_path = os.path.join(kitti_path, "velodyne",seq)
        calib_path = os.path.join(kitti_path, "calib",f"{seq}.txt")
        db_path = os.path.join(out_path, "gt_database",seq)
        os.system(f"mkdir -p {db_path}")        
        calib = kitti_utils.get_calib_from_file(calib_path)
        file_list = sorted(os.listdir(velodyne_path))
        objs = kitti_utils.get_objects_from_label(label_path, "track", calib, ds)
        
        framenum=int(file_list[-1][:-4])+1
        
        assert(framenum == len(file_list)), f"Frame number {framenum} not equal to file number {len(file_list)}"
            
        objs_frame = [[] for i in range(framenum)]
        for o in objs:
            try:
                objs_frame[o.frame_id].append(o)    
            except:
                print(o.frame_id)
                pdb.set_trace()

        data_info=[] 
        for i,l in enumerate(tqdm(file_list)):
            if(num >=0 and i >= num):
                break
            class_cnt={}
            fid = l[:-4]
            points =  np.fromfile(os.path.join(velodyne_path, fid+".bin"), dtype=np.float32).reshape(-1,4)
            for oid,obj in enumerate(objs_frame[i]):
                if(not obj.obj_type.lower() in CLASS_FILTER):
                    continue
                if(not obj.occlusion in OCC_FILTER):
                    continue
                
                if(obj.obj_type not in class_cnt):
                    class_cnt[obj.obj_type] = 0
                else:
                    class_cnt[obj.obj_type] += 1
                    
                file_name = f"{fid}_{obj.obj_type}_{class_cnt[obj.obj_type]}.bin"    
                # file_name = f"{fid}_{obj.obj_type}_{class_cnt[obj.obj_type]}_track_{obj.track_id}_occ_{obj.occlusion}.bin"
                in_points_flag = kitti_utils.points_in_box(points[:,:3], obj.box3d)      
                points_in_box = points[in_points_flag]  
                if(MIN_POINTS_FLAG and points_in_box.shape[0] < MIN_POINTS):   
                    skipcnt+=1
                    # data_info.append(get_info(obj, point_num, fid, file_name,i,oid))
                    continue
                center = np.array([obj.box3d['x'], obj.box3d['y'], obj.box3d['z']] )
                points_in_box[:, :3] -= center
                points_in_box.tofile(os.path.join(db_path,file_name))
                point_num = points_in_box.shape[0]
                data_info.append(get_info(obj, point_num, fid, file_name,i,oid))
                if(draw):
                    obj.box3d['x'], obj.box3d['y'], obj.box3d['z'] = 0,0,0
                    plot.draw_pcd_and_bbox(points_in_box,obj.box3d)
                    # print(obj.box3d)
                    # plot.draw_pcd_and_bbox(points,obj.box3d)
        print(f"Extract {len(data_info)} object and skip {skipcnt} low points object in {num} pcd and output to {db_path}")
        all_data_info[seq] = data_info       
    with open(os.path.join(out_path, "info.pkl"), 'wb') as file:
        pickle.dump(all_data_info, file)
   
def get_info(obj, point_num, fid, file_name,i,objid):    
    obj1 = deepcopy(obj.__dict__)
    obj1.pop('src')    
    try:
        obj1['box3d'].pop('corners_3d_cam')
        obj1['box3d'].pop('corners_org')
    except:
        pass
    info = {'obj':obj1, 'num_points_in_gt':point_num, 'velodyne_idx':fid, 'path':file_name,'gt_idx': i, 'obj_det_idx':objid}
    # print(info)
    return(info)

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines
if __name__ == "__main__":
    create_groundtruth_database()
