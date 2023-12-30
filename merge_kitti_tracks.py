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
    default="/home/philly12399/philly_data/pingtung-tracking-val/val/baseline/tracking/seq4/txt/",
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
    merge_tracks(inpath, outpath)


# merge kitti track label {i}.txt in same sequence to one label.txt
def merge_tracks(inpath, outpath):
    indir=sorted(os.listdir(inpath))
    tracks={}
    merged=""
    for i in indir:
        with open(os.path.join(inpath,i)) as fp:
            for line in fp:
                s1=line.split(" ")
                frame=int(s1[0])
                if not (frame in tracks):
                    tracks[frame]=""
                tracks[frame]=tracks[frame]+line
    for key in  sorted(tracks):
        merged=merged+tracks[key]
    os.system("mkdir -p {}".format(outpath))
    outfile = open(os.path.join(outpath,"label.txt"), "w")
    outfile.write(merged)
    outfile.close()


if __name__ == "__main__":
    main()
