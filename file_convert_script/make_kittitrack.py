import os
import sys
import click
@click.command()
### Add your options here
@click.option(
    "--pcd",
    "-p",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/filtered_seq/seq4",
    help="Path of pcd seq.",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/kitti-format/tracktest/",
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
    default="/home/philly12399/philly_data/pingtung-tracking-val/label.txt",
    help="Path of label",
)
@click.option(
    "--seq",
    "-s",
    type=int,
    default=4,
    help="seqnum",
)
@click.option(
    "--imgex",
    "-i",
    type=str,
    default="/home/philly12399/philly_utils/config/example.png",
    help="example image to fill image_02",
)
@click.option(
    "--clean",
    "-clean",
    type=bool,
    default=False,
    help="Clean previous output or not.",
)

def main(pcd, outpath, calib, label,seq,imgex, clean):
    if os.path.exists(outpath) and clean:
        os.system("rm -rf {}".format(outpath))
        print("clean")
    os.system("mkdir -p {}".format(outpath))
    seqstr=str(seq).zfill(4)
    pcdlistdir=sorted(os.listdir(pcd))
    num =len(pcdlistdir)
    # pcd2bin  velodyne

    binpath=os.path.join(outpath,"velodyne/"+seqstr)
    os.system("mkdir -p {}".format(binpath))
    os.system("python3 pcd_2_bin.py convert {} {} -1".format(pcd, binpath))
    os.system("python3 align_filename.py -p {} -e .bin -s 0".format(binpath))

    print("velodyne complete")
    # image
    imgpath=os.path.join(outpath,"image_02/"+seqstr)
    eximgpath=os.path.join(imgpath,"000000.png")
    os.system("mkdir -p {}".format(imgpath))
    os.system("cp {} {} ".format(imgex, eximgpath))
    for i in range(1, num):        
        os.system("ln  -f {} {}".format(eximgpath,os.path.join(imgpath, str(i).zfill(6)+'.png')))
    print("image complete")
    
    #label 
    #  Merge kitti tracks if you have many object tracks label file
    #  os.system("python3 merge_kitti_tracks -i {} -o {}".format())
    plist=sorted(os.listdir(pcd))
    labelpath=os.path.join(outpath,"label_02/")
    os.system("mkdir -p {}".format(labelpath))
    labelpath=os.path.join(labelpath, seqstr+".txt")
    os.system("cp {} {}".format(label,labelpath))
    print("label complete")
    
    # calib
    newcalibpath=os.path.join(outpath,"calib")
    os.system("mkdir -p {}".format(newcalibpath))
    newcalibpath = os.path.join(newcalibpath, seqstr+".txt")
    os.system("cp {} {}".format(calib,newcalibpath))
    print("calib complete")
    
    # seqmap
    seqmappath=os.path.join(outpath,"seqmap")
    os.system("mkdir -p {}".format(seqmappath))
    seqmappath = os.path.join(seqmappath, seqstr+".txt")
    outfile = open(seqmappath, "w")    
    msg=f"Range: {pcdlistdir[0]} ~ {pcdlistdir[-1]}\nTotal: {num} pcds \n"
    outfile.write(msg)
    outfile.close()
    print("seqmap complete")
    
    
if __name__ == "__main__":
    main()
