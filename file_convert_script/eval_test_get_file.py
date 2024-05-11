import os 
import click
#把label包裝給ab3dmot tracking eval
@click.command()
### Add your options here

@click.option(
    "--exp",
    "-e",
    type=str,
    default='track_new',
    help="path you want to align",
)
@click.option(
    "--output",
    "-o",
    type=str,
    default='/home/philly12399/evaltest/',
    help="path you want to align",
)
def get_file(exp,output):
    os.system(f"mkdir -p  {output}/{exp}/label")
    root = "/home/philly12399/thesis/AB3DMOT/results/Wayside/"
    label = os.path.join(root, "mark_Car_val_H1/data_0/")
    os.system(f"cp {label}/*  {output}/{exp}/label/")
    log = os.path.join(root, "log")
    latest_log = sorted(os.listdir(log))[-1]
    print(latest_log)
    os.system(f"cp {log}/{latest_log} {output}/{exp}/log.txt")
    
if __name__ == '__main__':
    get_file()
