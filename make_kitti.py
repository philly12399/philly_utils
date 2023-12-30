import os
import sys
import click
@click.command()
### Add your options here
@click.option(
    "--pcd",
    "-p",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/filtered_seq/",
    help="Path of pcd seq.",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/kitti-format/",
    help="output dir",
)
@click.option(
    "--calib",
    "-c",
    type=str,
    default="/home/philly12399/philly_utils/config/pingtung_w1.txt",
    help="Path of calib",
)
@click.option(
    "--label",
    "-l",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/baseline/detection/",
    help="Path of label",
)
@click.option(
    "--maxseq",
    "-m",
    type=int,
    default=4,
    help="maxseq convert",
)
@click.option(
    "--clean",
    "-clean",
    type=bool,
    default=False,
    help="Clean previous output or not.",
)

def main(pcd, outpath, calib, label,maxseq, clean):
    if os.path.exists(outpath) and clean:
        os.system("rm -rf {}".format(outpath))
        print("clean")
    os.system("mkdir -p {}".format(outpath))
    seqlist=sorted(os.listdir(pcd))
    count=0
    #skip sequence 
    skip=[1,2,3]
    for d in seqlist:
        count+=1
        if(count in  skip):
            print("skip ",count)
            continue

        if(count>maxseq):
            break
        outseqpath=os.path.join(outpath, d)
        os.system("mkdir -p {}".format(outseqpath))

        # pcd2bin  velodyne
        pcdpath=os.path.join(pcd, d)
        binpath=os.path.join(outseqpath,"velodyne")
        os.system("python3 pcd2bin.py convert {} {} -1".format(pcdpath, binpath))
       
        #label 
        plist=sorted(os.listdir(pcdpath))

        labelpath=os.path.join(label, d)
        newlabelpath=os.path.join(outseqpath,"label_2")
        os.system("cp -r  {} {}".format(labelpath,newlabelpath))
        for i, p in enumerate(sorted(os.listdir(newlabelpath))):
            f1=os.path.join(newlabelpath,p)
            f2=os.path.join(newlabelpath,plist[i][:6]+".txt")
            os.system("mv {} {}".format(f1,f2))

        
        # calib
        newcalibpath=os.path.join(outseqpath,"calib")
        os.system("mkdir -p {}".format(newcalibpath))
        for p in plist:     
            ncp=os.path.join(newcalibpath,p[:6]+".txt")
            os.system("cp  {} {}".format(calib,ncp))
        

    
if __name__ == "__main__":
    main()
