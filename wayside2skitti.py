import os
import sys
import click
@click.command()
### Add your options here
@click.option(
    "--datapath",
    "-d",
    type=str,
    default="/mnt/nfs/wayside_team/philly_data/0825ntu/",
    help="Path of wayside data.",
)
@click.option(
    "--exp",
    "-e",
    type=str,
    default="newdata",
    help="Name of experiment.",
)
@click.option(
    "--save",
    "-s",
    type=str,
    default="/home/philly12399/philly_data/",
    help="Parent directory of output data.",
)
@click.option(
    "--waysidenum",
    "-w",
    type=int,
    default=3,
    help="Which wayside you used?",
)
@click.option(
    "--numperseq",
    "-n",
    type=int,
    default=1000,
    help="How many number of pcds you want per seq?",
)
@click.option(
    "--clean",
    "-c",
    type=bool,
    default=False,
    help="Clean previous output or not.",
)
@click.option(
    "--bin",
    "-b",
    type=bool,
    default=True,
    help="Do pcd to bin or not. If you don't, you must make link under output.",
)
def main(datapath, exp, save,waysidenum,numperseq,clean, bin):
    CALIB="P0: 1 0 0 0 0 1 0 0 0 0 1 0\nP1: 1 0 0 0 0 1 0 0 0 0 1 0\nP2: 1 0 0 0 0 1 0 0 0 0 1 0\nP3: 1 0 0 0 0 1 0 0 0 0 1 0\nTr: 1 0 0 0 0 1 0 0 0 0 1 0\n"

    savepath = save+"/{}/skitti-format/sequences/".format(exp)
    if os.path.exists(savepath) and clean:
        os.system("rm -rf {}".format(savepath))
    if(waysidenum == -1):
        wayside = ""
    else:
        wayside = "wayside"+str(waysidenum)
    pcd_list=[]
    bin_list=[]
    for d in os.listdir(datapath):
        d = os.path.join(datapath, d)
        TIMESTAMP = os.path.basename(d)
        
        if TIMESTAMP == "@eaDir" or TIMESTAMP[:6] == "skitti":
            continue

        print(d)
        
        
        inpath = os.path.join(d, wayside)
        outpath = os.path.join(savepath, TIMESTAMP)
        if os.path.exists(outpath) and clean:
            os.system("rm -rf {}".format(outpath))
        os.makedirs(outpath,exist_ok=True)
        if(bin):
            os.system("python3 pcd2bin.py convert {} {} -1".format(inpath, outpath))
        else:
            outpath = os.path.join(outpath,"velodyne")
        bin_list.append(outpath)
        pcd_list.append(inpath)

    base=0
    for bi in range(len(bin_list)):
        b=bin_list[bi]
        l=os.listdir(b)
        for i in range(0,len(l),numperseq):
            iend=min(i+numperseq,len(l))
            format_base = "{:02d}".format(base)
            outpath = os.path.join(savepath, format_base)
            vpath = os.path.join(outpath,'velodyne')
            os.makedirs(outpath,exist_ok=True)
            os.makedirs(vpath,exist_ok=True)
            for j in range(i,iend):
                s1=os.path.join(b,"{:06d}.bin".format(j))
                s2=os.path.join(vpath,"{:06d}.bin".format(j))
                os.system("ln -sf {} {}".format(s1, s2))
            with open(os.path.join(outpath, "timestamp.txt"), "w") as timestamp_file:
                timestamp_file.write("FROM:{}\nFrame:{} ~ {}".format(pcd_list[bi], i, iend-1))
                print("Put Frame:{} ~ {} in SEQ {}".format(i, iend-1, format_base))
            with open(os.path.join(outpath, "calib.txt"), "w") as calib_file:
                calib_file.write("{}".format(CALIB))
            open(os.path.join(outpath, "times.txt"), "w").close()
            base+=1
if __name__ == "__main__":
    main()
