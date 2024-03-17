import os
import numpy as np
import click
from tqdm import tqdm

def read_pcd(filepath,filt):
    lidar = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        field_ind=-2
        #Field
        field = lines[2].replace('\n','').split(' ')[1:]
        if('active' in field):
            field_ind = field.index("active")
        for line in lines[11:]:
            linestr = line.replace('\n','').split(" ")
            if(filt and field_ind >= 0):
                if (linestr[field_ind]=='0'):
                    continue
            linestr_convert = list(map(float, linestr[:3]))
            linestr_convert.append(0)
            lidar.append(linestr_convert)
    return np.array(lidar)

@click.command()
### Add your options here
@click.option(
    "--pcdfolder",
    "-p",
    type=str,
    required=True,
    help="Path of input pcd",
)
@click.option(
    "--binfolder",
    "-b",
    type=str,
    required=True,
    help="Path of output bin",
)
@click.option(
    "--convert_number",
    "-n",
    type=int,
    default=-1,
    help="convert number",
)
@click.option(
    "--filt",
    "-f",
    type=bool,
    default=False,
    help="Clean previous output or not.",
)

def convert(pcdfolder, binfolder, convert_number,filt):
        
    if(convert_number == -1):
        convert_number = 99999999
    file_list = os.listdir(pcdfolder)
    file_list.sort()
    count = 0
    if os.path.exists(binfolder):
        pass
    else:
        os.makedirs(binfolder)
    convert_number = min(convert_number,len(file_list))
    print("Total: ", len(file_list)," pcds")
    print("Convert: ", convert_number, " pcds")
    print(f"Filt inactive points: {filt}")
    file_list = file_list[:convert_number]
    for (count,file) in  enumerate(tqdm(file_list, desc="Converting")):     
        (filename, extension) = os.path.splitext(file)
        if extension == ".pcd" and count < convert_number:
            velodyne_file = os.path.join(pcdfolder, filename) + '.pcd'
            pl = read_pcd(velodyne_file, filt)
            pl = pl.reshape(-1, 4).astype(np.float32)
            velodyne_file_new = os.path.join(binfolder, filename) + '.bin'
            pl.tofile(velodyne_file_new)
        
        


if __name__ == "__main__":
    convert()
