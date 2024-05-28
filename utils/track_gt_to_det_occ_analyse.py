import numpy as np
import os
import click
import pdb
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
    "--out_path",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/KITTI_tracking/training/gt_det_set_v2/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of output.",
)
@click.option(
    "--difficulty",
    "-d",
    type=int,
    default=3,
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Difficulty of dataset.",
)
def main(gt_path,out_path,difficulty):
    np.random.seed(0)    
    # convert(gt_path,"0021.txt",'wayside',out_path)
    if   (difficulty==0): args=({},0,0,0)
    elif (difficulty==1): args=({2,3},5,5,0.3)
    elif (difficulty==2): args=({2,3},5,5,0.6)
    elif (difficulty==3): args=({2,3},5,5,1.0)
    elif (difficulty==4): args=({2,3},0,0,1.0)
    else : assert False
    # out_path = os.path.join(out_path,f"diff{difficulty}")
    # os.system(f"mkdir -p {out_path}")
    
    filt_cnt = {}
    CLS= ["cyclist"]
    print(f"Occlude sequence analyse for {CLS}, OCC:{args[0]}")
    for s in sorted(os.listdir(gt_path)):  
        if(s=="0021.txt"): filt_cnt[s] = convert(gt_path,s,'wayside',out_path,args,CLS)
        else:
            filt_cnt[s] = convert(gt_path,s,'kitti',out_path,args,CLS)
        print(f"{s}: {filt_cnt[s]}")
    # buf = ""
    # buf+=f"Difficulty: {difficulty}, With args OCC_FILTER: {args[0]},  birth_buf: {args[1]},  death_buf: {args[2]},  drop_rate: {args[3]}\n"
    # for s in filt_cnt:
    #     buf+=f"{s} filt {filt_cnt[s]} objects\n"
    # log_path = os.path.join(out_path,'log.txt')
    # with open (log_path,"w") as f:
    #     f.write(buf)
        
def convert(gt_path,filename,format,output, filter_args,CLS):
    format = format.lower()
    file_path = os.path.join(gt_path,filename)
    output = os.path.join(output,filename)
    # print(f"convert {file_path} to {output} with format {format}") 
    
    data_by_trackid = collect_data(file_path,format,CLS)
    # filted_data, filt_cnt,all_cnt = data_filter_rand_drop(data_by_trackid, *filter_args)
    # filted_data, filt_cnt,all_cnt = data_filter_seq_drop(data_by_trackid, *filter_args)    
    return data_filter_seq_drop(data_by_trackid, *filter_args)
    
    ii=-1
    buffer = ""
    for d in filted_data:
        assert d[0]!= ii
        buffer+=d[1]
        ii = d[0]
    with open(output, 'w') as f:
        f.write(buffer)
    # all_cnt = len(filted_data)
    return f"{filt_cnt} / {all_cnt}"

def collect_data(file_path,format,CLS):
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
                cls2id=CLS
                # cls2id={'car':2,'cyclist':3}
                neighbor = {'van':'car','truck':'car'}
            elif format == "wayside":
                cls2id=CLS               
                # cls2id={'car':1,'cyclist':2}
                neighbor = {'truck':'car'}
            else: assert False
            
            x[2] = x[2].lower()
            if(x[2] in neighbor): x[2] = neighbor[x[2]]
            if(x[2] not in cls2id): continue                    
            x[2] = x[2].capitalize()
            tmpcls=x[2]           
                     
            tid=int(x[1])
            if(tid not in data_by_trackid):
                data_by_trackid[tid]=[]
            x[1] = -1 
            det= ""
            for xi in x:
                det+=f"{str(xi)} "
            det+="1.0\n" #score
            filtbuf=""
            x[2] = "Filtered"+x[2]
            for xi in x:
                filtbuf+=f"{str(xi)} "
            filtbuf+="1.0\n" #score
            data_by_trackid[tid].append({'i':fi, 'trunc':trunc,'occ':occ,'buf':det,'filtbuf':filtbuf, 'class':tmpcls})
    return data_by_trackid

def data_filter_seq_drop(data_by_trackid, OCC_FILTER={}, birth_buf=0, death_buf=0, drop_rate=1.0):
    filted_data=[]
    filt_cnt={'car':0,'cyclist':0}
    all_cnt ={'car':0,'cyclist':0}
    total_len=0
    total_cnt=0
    for tid in data_by_trackid:
        trk = data_by_trackid[tid]
        num = len(trk)
        trk_occ_seq = []
        cur_occ_seq = []    
        #collect occlude seq of each track                
        for i,d in enumerate(trk):
            if(d['occ'] in OCC_FILTER) and (not in_range(i,0,birth_buf)) and (not in_range(i,num-death_buf,num)):
                cur_occ_seq.append(i)
            else:
                if cur_occ_seq:
                    trk_occ_seq.append(cur_occ_seq)
                    cur_occ_seq = []
        if cur_occ_seq:
            trk_occ_seq.append(cur_occ_seq)
        for c in trk_occ_seq:
            total_len+=len(c)
            total_cnt+=1
    try:
        avg_occ_len = round(total_len/total_cnt,1)
    except:
        avg_occ_len=0
        
    log=f'avg_occ_len: {avg_occ_len:<5}, total_occ_seq:{total_cnt:<5}, total_object:{len(data_by_trackid):<5}'
    return log


def in_range(x,l,r): #[l,r)
    return x>=l and x<r



if __name__ == "__main__":
    main()