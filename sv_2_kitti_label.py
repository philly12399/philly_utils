import os
import sys
import click
import json
@click.command()
### Add your options here
@click.option(
    "--sv",
    "-s",
    type=str,
    default="/home/philly12399/philly_data/pingtung-tracking-val/sv/pingtungw1_seq4_episodes",
    # default="/home/philly12399/svtest",

    help="Path of sv episodes",
)
@click.option(
    "--outpath",
    "-o",
    type=str,
    default="/home/philly12399/philly_data/sv_out",
    help="Path of output",
)
@click.option(
    "--clean",
    "-clean",
    type=bool,
    default=False,
    help="Clean previous output or not.",
)
@click.option(
    "--mode",
    "-m",
    type=str,
    default="all",
    help="kitti label mode  one or all(one obj / all obj one file)",
)
def main(sv, outpath, clean, mode):
    if os.path.exists(outpath) and clean:
        os.system("rm -rf {}".format(outpath))
        print("clean")
    os.system("mkdir -p {}".format(outpath))
    sv_episodes = sv_parse(sv)
    sv2kittilabel(sv_episodes, outpath, mode)

def sv_parse(sv):
    l = os.listdir(sv)
    sv_episodes={}
    key_id_map = open(os.path.join(sv,"key_id_map.json"))
    meta = open(os.path.join(sv,"meta.json"))
    datasets=[]
    sv_episodes['key_id_map']=json.load(key_id_map)
    sv_episodes['meta']=json.load(meta)
    data_json={}
    for i in l:
        p = os.path.join(sv,i)
        if(os.path.isdir(p)):
            datasets.append(p)
            data_json[i]={'name':i}
    for dataset in datasets:
        basename = os.path.basename(dataset)
        annotation =  open(os.path.join(dataset,"annotation.json"))
        frame_pointcloud_map = open(os.path.join(dataset,"frame_pointcloud_map.json"))
        data_json[basename]["annotation"] = json.load(annotation)
        data_json[basename]["frame_pointcloud_map"] = json.load(frame_pointcloud_map)
    sv_episodes['datasets']=data_json
    return sv_episodes       

def sv2kittilabel(sv_episodes, outpath, mode):
    for key in sv_episodes['datasets']:
        data = sv_episodes['datasets'][key]
        name = data["name"]
        ann = data["annotation"]
        fpmap = data["frame_pointcloud_map"]
        kitti_outpath = os.path.join(outpath, name+"_kitti")
        os.system("mkdir -p {}".format(kitti_outpath))
        obj={}
        allobj=""
        id1 = 0
        for o in ann["objects"]:
            obj[o["key"]] = {"class":o["classTitle"], "id":id1, "bboxes":"" }
            id1+=1
        for frame in ann["frames"]:
            fid = index2fid(frame["index"], fpmap)
            for bbox in frame["figures"]:
                k = bbox["objectKey"]
                bd=bbox["geometry"]["dimensions"]
                euler=bbox["geometry"]["rotation"]["z"]
                bp=bbox["geometry"]["position"]
                obj[k]["bboxes"]+=f"{frame['index']} {obj[k]['id']} {obj[k]['class']} 0 0 0 0 0 0 0 {bd['x']} {bd['y']} {bd['z']} {bp['x']} {bp['y']} {bp['z']} {euler}\n"
                allobj+=f"{frame['index']} {obj[k]['id']} {obj[k]['class']} 0 0 0 0 0 0 0 {bd['x']} {bd['y']} {bd['z']} {bp['x']} {bp['y']} {bp['z']} {euler}\n"
        if(mode=='all'):
            filename =  f"label.txt"
            outfile = open(os.path.join(kitti_outpath,filename), "w")
            outfile.write(allobj)
            outfile.close()
        elif(mode=='one'):
            for objkey in obj:
                o=obj[objkey]
                filename =  f"{o['id']:06d}"+'.txt' 
                outfile = open(os.path.join(kitti_outpath,filename), "w")
                outfile.write(o['bboxes'])
                outfile.close()
        


def index2fid(index, fpmap):
    return int(fpmap[str(index)][:-4])

if __name__ == "__main__":
    main()
