import numpy as np
import os
import click
import pdb
import math
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
    default="/home/philly12399/philly_data/KITTI_tracking/training/gt_det_set_v2/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of output.",
)
@click.option(
    "--difficulty",
    "-d",
    type=int,
    default=4,
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Difficulty of dataset.",
)
@click.option(
    "--mode",
    "-m",
    type=str,
    default="rand",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="mode of drop rand or seq",
)
def main(gt_path,format,out_path,difficulty,mode):
    np.random.seed(0)    
    assert mode == "seq" or mode == "rand", "mode must be seq or rand"

    #args: OCC_FILTER,BD_BUF,DROP_RATE of car/cyclist
    if   (difficulty==0): args={'car':({},0,0)     ,'cyclist':({},0,0)}
    elif (difficulty==1): args={'car':({2,3},5,0.3),'cyclist':({},0,0)}
    elif (difficulty==2): args={'car':({2,3},5,0.6),'cyclist':({},0,0)}
    elif (difficulty==3): args={'car':({2,3},5,1.0),'cyclist':({},0,0)}
    elif (difficulty==4): args={'car':({2,3},0,1.0),'cyclist':({},0,0)}
    else : assert False
    out_path = os.path.join(out_path,f"diff{difficulty}")
    os.system(f"mkdir -p {out_path}")
    
    filt_cnt = {}
    for s in sorted(os.listdir(gt_path)):  
        if(s=="0021.txt"): filt_cnt[s] = convert(gt_path,s,'wayside',out_path,mode, args)
        else:
            filt_cnt[s] = convert(gt_path,s,'kitti',out_path,mode, args)
    log_prefix = f"Difficulty: {difficulty}, Mode: {mode} drop\n"
    for c in args:
        arg=args[c]
        log_prefix+=f"With {c} args OCC_FILTER: {arg[0]},  BD_BUF: {arg[1]}, DROP_RATE: {arg[3]}\n"
    write_log(filt_cnt,args,out_path,log_prefix)
    
 
def convert(gt_path,filename,format,output,mode,args):
    format = format.lower()
    file_path = os.path.join(gt_path,filename)
    output = os.path.join(output,filename)
    # print(f"convert {file_path} to {output} with format {format}") 
    
    data_by_trackid = collect_data(file_path,format)
    if(mode == "rand"):
        filted_data, filt_cnt,all_cnt = data_filter_rand_drop(data_by_trackid, args)
    elif(mode == "seq"):
        filted_data, filt_cnt,all_cnt = data_filter_seq_drop(data_by_trackid, args)    
    
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

def collect_data(file_path,format):
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
            elif format == "wayside":
                cls2id={'car':1,'cyclist':2}
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
            data_by_trackid[tid].append({'line':fi, 'trunc':trunc,'occ':occ,'buf':det,'filtbuf':filtbuf, 'class':tmpcls})
    return data_by_trackid

def data_filter_rand_drop(data_by_trackid,args):
    #arg parser and stat counter
    OCC_FILTER,BD_BUF,DROP_RATE={},{},{}
    filt_cnt,all_cnt={},{}
    for c in args:
        OCC_FILTER[c] = args[c][0]
        BD_BUF[c] = args[c][1]
        DROP_RATE[c] = args[c][2]
        filt_cnt[c]=0
        all_cnt[c]=0
    
    filted_data=[]    
    for tid in data_by_trackid:
        trk = data_by_trackid[tid]
        num = len(trk)
        for di, d in enumerate(trk):
            # print(di,num)
            c = d['class'].lower()
            all_cnt[c]+=1
            data_line = (d['line'],d['buf'])
            if(d['occ'] in OCC_FILTER[c]):
                if((not in_range(di,0,BD_BUF[c])) and (not in_range(di,num-BD_BUF[c],num))):
                    # drop 
                    if(random_drop(DROP_RATE[c])):                         
                        filt_cnt[c]+=1
                        data_line = (d['line'],d['filtbuf'])
            filted_data.append(data_line)
    filted_data = sorted(filted_data, key=lambda x: x[0])
    return filted_data,filt_cnt,all_cnt

def data_filter_seq_drop(data_by_trackid,args):
     #arg parser and stat counter
    OCC_FILTER,BD_BUF,DROP_RATE={},{},{}
    filt_cnt,all_cnt={},{}
    for c in args:
        OCC_FILTER[c] = args[c][0]
        BD_BUF[c] = args[c][1]
        DROP_RATE[c] = args[c][2]
        filt_cnt[c]=0
        all_cnt[c]=0
        
    filted_data=[]
    for tid in data_by_trackid:
        trk = data_by_trackid[tid]
        num = len(trk)
        trk_occ_seq = []
        cur_occ_seq = []    
        c = trk[0]['class'].lower()
        #collect occlude seq of each track                
        for i,d in enumerate(trk):            
            # in occ filter and not in birth/death buf
            if(d['occ'] in OCC_FILTER[c]) and ((not in_range(i,0,BD_BUF[c])) and (not in_range(i,num-BD_BUF[c],num))):
                    cur_occ_seq.append(i)
            else:
                if cur_occ_seq:
                    trk_occ_seq.append(cur_occ_seq)
                    cur_occ_seq = []              
        if cur_occ_seq:
            trk_occ_seq.append(cur_occ_seq)

        ## random seq drop 
        drop_id = []
        for occ_seq in trk_occ_seq:
            #RAND
            # for i in range(len(occ_seq)):
            #     if(random_drop(DROP_RATE[c])):          
            #         drop_id.append(i)
            #SEQ
            dropx = int(math.ceil(len(occ_seq)*DROP_RATE[c]))
            drop_id.extend(random_subsequence(occ_seq,dropx))
            
        #append filterd trk to result    
        for di, d in enumerate(trk):
            # print(di,num)
            all_cnt[c]+=1
            if(di  in drop_id):
                filt_cnt[c]+=1
                data_line = (d['line'],d['filtbuf'])
            else:
                data_line = (d['line'],d['buf'])                
            filted_data.append(data_line)
            
    filted_data = sorted(filted_data, key=lambda x: x[0])
    return filted_data,filt_cnt,all_cnt

def random_drop(p):
    x=np.random.rand()
    return x < p

def in_range(x,l,r): #[l,r)
    return x>=l and x<r

def random_subsequence(sequence, x):
    l = len(sequence)
    if x > l:
        raise ValueError("子序列的長度不能大於輸入序列的長度")
    # 生成隨機起始位置
    start_index = np.random.choice(l - x + 1)
    return sequence[start_index:start_index + x]

def write_log(filt_cnt,args,out_path,log_prefix):
    buf=log_prefix
    #With args OCC_FILTER: {args[0]},  birth_buf: {args[1]},  death_buf: {args[2]},  drop_rate: {args[3]}
    for s in filt_cnt:
        buf+=f"{s} filt {filt_cnt[s]} objects\n"
    log_path = os.path.join(out_path,'log.txt')
    with open (log_path,"w") as f:
        f.write(buf)
        
if __name__ == "__main__":
    main()