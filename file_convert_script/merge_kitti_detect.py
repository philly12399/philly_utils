import os
import sys
import click
import json
@click.command()
### Add your options here
@click.option(
    "--inpath",
    "-i",
    type=str,
    default="/home/philly12399/philly_data/KT_output/0001",
    help="Path of labels",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/KT_output",
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
    merge_dets(inpath, outpath, exp)


# merge kitti track label {i}.txt in same sequence to one label.txt
def merge_dets(inpath, outpath,exp):
    indir=sorted(os.listdir(inpath))
    dets={}
    merged=""
    f=0
    buf=""
    for i in indir:
        with open(os.path.join(inpath,i)) as fp:
            for line in fp:
                s = f"{f} -1 {line}"
                buf+=s
        f += 1
    os.system("mkdir -p {}".format(outpath))
    outfile = open(os.path.join(outpath,f"{exp}.txt"), "w")
    outfile.write(buf)
    outfile.close()


if __name__ == "__main__":
    main()
