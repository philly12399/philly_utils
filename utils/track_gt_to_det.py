import numpy as np
import os
import click
@click.command()
@click.option(
    "--gt_path",
    "-g",
    type=str,
    default="/home/philly12399/philly_data/KITTI_tracking/training/labels/label_gt/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of track gt.",
)
@click.option(
    "--format",
    "-f",
    type=str,
    default="kitti",
    help="output format, kitti/wayside",
)
@click.option(
    "--out_path",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/KITTI_tracking/training/gt_det_set/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of output.",
)
@click.option(
    "--difficulty",
    "-d",
    type=int,
    default=0,
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Difficulty of dataset.",
)
def main(gt_path,format,out_path,difficulty):
    np.random.seed(0)    
    # convert(gt_path,"0021.txt",'wayside',out_path)
    if   (difficulty==0): args=({},0,0,0)
    elif (difficulty==1): args=({2,3},5,5,0.3)
    elif (difficulty==2): args=({2,3},5,5,0.6)
    elif (difficulty==3): args=({2,3},5,5,1.0)
    elif (difficulty==4): args=({2,3},0,0,1.0)
    else : assert False
    out_path = os.path.join(out_path,f"diff{difficulty}")
    os.system(f"mkdir -p {out_path}")
    
    filt_cnt = {}
    for s in sorted(os.listdir(gt_path)):  
        if(s=="0021.txt"): filt_cnt[s] = convert(gt_path,s,'wayside',out_path,*args)
        else:
            filt_cnt[s] = convert(gt_path,s,'kitti',out_path,*args)
        
    buf = ""
    buf+=f"Difficulty: {difficulty}, With args OCC_FILTER: {args[0]},  birth_buf: {args[1]},  death_buf: {args[2]},  drop_rate: {args[3]}\n"
    for s in filt_cnt:
        buf+=f"{s} filt {filt_cnt[s]} objects\n"
    log_path = os.path.join(out_path,'log.txt')
    with open (log_path,"w") as f:
        f.write(buf)
        
def convert(gt_path,filename,format,output, OCC_FILTER={}, birth_buf=0, death_buf=0, drop_rate=1.0):
    format = format.lower()
    file_path = os.path.join(gt_path,filename)
    output = os.path.join(output,filename)
    print(f"convert {file_path} to {output} with format {format}") 
    data_by_trackid={}
    ##collect data of target class
    with open(file_path, "r") as f:
        for fi,line in enumerate(f):
            x = line.strip().split(' ')
            tid=int(x[1])
            trunc=int(x[3])                
            occ=int(x[4])
            # if(occ in OCC_FILTER):
            #     continue
            if format == "kitti":
                cls2id={'car':2,'cyclist':3}
                neighbor = {'van':'car','truck':'car'}
                x[2] = x[2].lower()
                if(x[2] in neighbor): x[2] = neighbor[x[2]]
                if(x[2] not in cls2id): continue                    
                
                if(tid not in data_by_trackid):
                    data_by_trackid[tid]=[]   
                              
                frame=x[0]
                clsid = cls2id[x[2]]
                bbox2d=f"{x[6]},{x[7]},{x[8]},{x[9]}"
                bbox3d=f"{x[10]},{x[11]},{x[12]},{x[13]},{x[14]},{x[15]},{x[16]}"
                alpha = x[5]
                score=1.0                
                det = f"{frame},{clsid},{bbox2d},{score},{bbox3d},{x[5]}\n"
                filtbuf = f"{frame},{-1},{bbox2d},{score},{bbox3d},{x[5]}\n"
            elif format == "wayside":
                tid=int(x[1])
                if(tid not in data_by_trackid):
                    data_by_trackid[tid]=[]
                x[1] = -1 #track_id
                # x[3],x[4],x[5] = 0, 0, 0.0 #truncated,occluded,alpha
                det= ""
                for xi in x:
                    det+=f"{str(xi)} "
                det+="1.0\n" #score
                filtbuf=""
                x[2] = "Filtered"
                for xi in x:
                    filtbuf+=f"{str(xi)} "
                filtbuf+="1.0\n" #score
            else:
                assert False 
            data_by_trackid[tid].append({'i':fi, 'trunc':trunc,'occ':occ,'buf':det,'filtbuf':filtbuf})
    filted_data=[]
    filt_cnt=0
    for tid in data_by_trackid:
        trk = data_by_trackid[tid]
        num = len(trk)
        for di, d in enumerate(trk):
            # print(di,num)
            data_line = (d['i'],d['buf'])
            if(d['occ'] in OCC_FILTER):
                if((not in_range(di,0,birth_buf)) and (not in_range(di,num-death_buf,num))):
                    # drop 
                    if(random_drop(drop_rate)): 
                        filt_cnt+=1
                        data_line = (d['i'],d['filtbuf'])
            filted_data.append(data_line)
            
    filted_data = sorted(filted_data, key=lambda x: x[0])
    ii=-1
    buffer = ""
    for d in filted_data:
        assert d[0]!= ii
        buffer+=d[1]
        ii = d[0]
    with open(output, 'w') as f:
        f.write(buffer)
    all_cnt = len(filted_data)
    return f"{filt_cnt} / {all_cnt}"

def random_drop(p):
    x=np.random.rand()
    return x < p

def in_range(x,l,r): #[l,r)
    return x>=l and x<r

if __name__ == "__main__":
    main()