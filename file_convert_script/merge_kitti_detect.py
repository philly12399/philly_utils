import os
import sys
import click
import json
#把多個kittidetect label file merge成一個kittitrack label
@click.command()
### Add your options here
@click.option(
    "--inpath",
    "-i",
    type=str,
    default="/home/philly12399/philly_ssd/KITTI_tracking/training/kitti_detection/second_iou/training",
    help="Path of labels",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_ssd/KITTI_tracking/training/merged_det/second_iou",
    help="Path of output",
)
@click.option(
    "--exp",
    "-e",
    type=str,
    default='label',
    help="path you want to align",
)
def main(inpath, outpath,exp):
    indirs=sorted(os.listdir(inpath))
    for d in indirs:
        in1=os.path.join(inpath,d)
        merge_dets(in1, outpath, d)


# merge kitti track label {i}.txt in same sequence to one label.txt
def merge_dets(inpath, outpath,exp):
    indir=sorted(os.listdir(inpath))
    dets={}
    merged=""
    f=0
    buf=""
    clsdict={}
    print(f"merge {inpath} to {outpath}/{exp}.txt")
    for i in indir:
        with open(os.path.join(inpath,i)) as fp:
            for line in fp:
                col=line.split(" ")
                if(len(col)<16):
                    continue
                c=line.split(" ")[0]
                if(c not in clsdict):
                    clsdict[c]=0
                clsdict[c]+=1                
                s = f"{f} -1 {line}"
                buf+=s
        f += 1
    os.system("mkdir -p {}".format(outpath))
    outfile = open(os.path.join(outpath,f"{exp}.txt"), "w")
    print(clsdict)
    outfile.write(buf)
    outfile.close()


if __name__ == "__main__":
    main()
