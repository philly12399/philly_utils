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
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/baseline/detection/seq4/",
    help="Path of labels",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/sv_out/",
    help="Path of output",
)

def main(inpath, outpath):
    merge_dets(inpath, outpath)


# merge kitti track label {i}.txt in same sequence to one label.txt
def merge_dets(inpath, outpath):
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
    outfile = open(os.path.join(outpath,"label.txt"), "w")
    outfile.write(buf)
    outfile.close()


if __name__ == "__main__":
    main()
