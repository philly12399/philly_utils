import os 
import click
import merge_kitti_detect
#把detect label提出
@click.command()
### Add your options here

@click.option(
    "--detect",
    "-d",
    type=str,
    default='/home/philly12399/philly_data/KT_output/KT_det_all',
    help="path you want to align",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default='/home/philly12399/philly_data/KT_output/label_all_0512',
    help="path you want to align",
)
def get_file(detect,output):
    latest_det = []
    seq_name = []    
    for seq in sorted(os.listdir(detect)):
        seq_path = os.path.join(detect, seq)
        print(seq_path)
        dirs = sorted([os.path.join(seq_path,item) for item in os.listdir(seq_path)])
        dirs = [d for d in dirs if os.path.isdir(d)]
        latest_det.append(dirs[-1])
        seq_name.append(seq)
    for i,s in enumerate(seq_name):
        merge_kitti_detect.merge_dets(latest_det[i],output,s)
        
if __name__ == '__main__':
    get_file()
