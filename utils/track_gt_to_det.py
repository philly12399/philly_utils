import numpy as np
import os
import click
@click.command()
@click.option(
    "--gt_path",
    "-g",
    type=str,
    default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",
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
    default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt_det_occ0_occ1/",
    # default="/home/philly12399/philly_data/KITTI_tracking/training/label_gt/",    
    help="Path of output.",
)
def main(gt_path,format,out_path):
    os.system(f"mkdir -p {out_path}")
    # convert(gt_path,"0021.txt",'wayside',out_path)
    for s in sorted(os.listdir(gt_path)):          
        convert(gt_path,s,'kitti',out_path)
            
def convert(gt_path,filename,format,output):
    file_path = os.path.join(gt_path,filename)
    output = os.path.join(output,filename)
    buffer = ""
    print(f"convert {file_path} to {output} with format {format}") 
    OCC_FILTER={2,3}
    with open(file_path, "r") as f:
        for line in f:
            x = line.strip().split(' ')
            trunc=int(x[3])                
            occ=int(x[4])
            if(occ in OCC_FILTER):
                continue
            if format.lower() == "kitti":
                cls2id={'car':2,'cyclist':3}
                neighbor = {'van':'car','truck':'car'}
                x[2] = x[2].lower()
                if(x[2] in neighbor): x[2] = neighbor[x[2]]
                if(x[2] not in cls2id): continue                
                frame=x[0]
                clsid = cls2id[x[2]]
                bbox2d=f"{x[6]},{x[7]},{x[8]},{x[9]}"
                bbox3d=f"{x[10]},{x[11]},{x[12]},{x[13]},{x[14]},{x[15]},{x[16]}"
                alpha = x[5]
                score=1.0                
                det = f"{frame},{clsid},{bbox2d},{score},{bbox3d},{x[5]}\n"
            elif format.lower() == "wayside":
                x[1] = -1 #track_id
                # x[3],x[4],x[5] = 0, 0, 0.0 #truncated,occluded,alpha
                det= ""
                for xi in x:
                    det+=f"{str(xi)} "
                det+="1.0\n" #score
            else:
                assert False 
            buffer+=det
    with open(output, 'w') as f:
        f.write(buffer)
    
if __name__ == "__main__":
    main()