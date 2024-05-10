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
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/kitti-format/ttt/",
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
        pcdlistdir = sorted(os.listdir(pcdpath))
        num = len(pcdlistdir)
        binpath=os.path.join(outseqpath,"velodyne")
        os.system("python3 pcd_2_bin.py convert {} {} -1".format(pcdpath, binpath))
        os.system("python3 align_filename.py -p {} -e .bin -s 0".format(binpath))
        #label 
        plist=sorted(os.listdir(pcdpath))

        labelpath=os.path.join(label, d)
        newlabelpath=os.path.join(outseqpath,"label_2")
        os.system("cp -r  {} {}".format(labelpath,newlabelpath))
        # for i, p in enumerate(sorted(os.listdir(newlabelpath))):
        #     f1=os.path.join(newlabelpath,p)
        #     f2=os.path.join(newlabelpath, str(i).zfill(6) + ".txt")
        #     os.system("mv {} {}".format(f1,f2))

        
        # calib
        newcalibpath=os.path.join(outseqpath,"calib")
        os.system("mkdir -p {}".format(newcalibpath))
        for i in range(num):     
            ncp=os.path.join(newcalibpath, str(i).zfill(6) + ".txt")
            os.system("cp  {} {}".format(calib,ncp))
            
        # seqmap
        seqmappath=os.path.join(outseqpath,"seqmap")
        os.system("mkdir -p {}".format(seqmappath))
        seqmappath = os.path.join(seqmappath, "seqmap.txt")
        outfile = open(seqmappath, "w")    
        msg=f"Range: {pcdlistdir[0]} ~ {pcdlistdir[-1]}\nTotal: {num} pcds \n"
        outfile.write(msg)
        outfile.close()
        print("seqmap complete")

    
if __name__ == "__main__":
    main()
