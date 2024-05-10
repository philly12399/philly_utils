import os
import sys
import click
@click.command()
### Add your options here
@click.option(
    "--velopath",
    "-v",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/filtered_seq/seq4/",
    help="Path of input velodyne ",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/skitti-format/filtered_seq/04/",
    help="Path of skitti output.",
)


def main(velopath,outpath):
    CALIB="P0: 1 0 0 0 0 1 0 0 0 0 1 0\nP1: 1 0 0 0 0 1 0 0 0 0 1 0\nP2: 1 0 0 0 0 1 0 0 0 0 1 0\nP3: 1 0 0 0 0 1 0 0 0 0 1 0\nTr: 1 0 0 0 0 1 0 0 0 0 1 0\n"
    os.system("mkdir -p {}".format(outpath))
    outvelopath=os.path.join(outpath,"velodyne")
    os.system("mkdir -p {}".format(outvelopath))
    
    l=sorted(os.listdir(velopath))
    if(l[0][-4:]==".bin"):
        for i in l:
            a=os.path.join(velopath,i)
            b=os.path.join(outvelopath,i)
            os.system(f"ln -f {a} {b}")
    elif(l[0][-4:]==".pcd"):
        os.system("python3 pcd_2_bin.py convert {} {} -1".format(velopath, outvelopath))
    else:
        print(f"{l[0]} wrong format")
        exit()
    # with open(os.path.join(outpath, "timestamp.txt"), "w") as timestamp_file:
    #     timestamp_file.write("FROM:{}\nFrame:{} ~ {}".format(pcd_list[bi], i, iend-1))
    #     print("Put Frame:{} ~ {} in SEQ {}".format(i, iend-1, format_base))
    with open(os.path.join(outpath, "calib.txt"), "w") as calib_file:
        calib_file.write("{}".format(CALIB))
    open(os.path.join(outpath, "times.txt"), "w").close()

if __name__ == "__main__":
    main()
