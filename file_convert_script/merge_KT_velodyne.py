import os 
import click
from tqdm import tqdm
#把KT velodyne seq包成一個
@click.command()
### Add your options here

@click.option(
    "--kitti",
    "-k",
    type=str,
    default='/home/philly12399/philly_data/KITTI_tracking/training/',
    help="kittti root",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default='merged_velodyne',
    help="output name",
)
def merge_seq(kitti,output):
    kitti_velodyne = os.path.join(kitti,"velodyne")
    seqlist = sorted(os.listdir(kitti_velodyne))
    output = os.path.join(kitti,output)
    os.system(f"mkdir -p {output}")
    for s in tqdm(seqlist):
        seq_path = os.path.join(kitti_velodyne,s)
        bin_list = os.listdir(seq_path)
        for f in tqdm(bin_list):
            newid = f"{s}_{f}"
            origin = os.path.join(seq_path,f)            
            link = os.path.join(output,newid)
            os.system(f"ln -f {origin} {link}")
            
    
if __name__ == '__main__':
    merge_seq()
