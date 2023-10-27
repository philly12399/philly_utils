from os import listdir,rename
from os.path import isfile, join
import click
@click.command()
### Add your options here
@click.option(
    "--path",
    "-p",
    type=str,
    required=True,
    help="path you want to align",
)
@click.option(
    "--extension",
    "-e",
    type=str,
    default=".bin",
    help="file extension you want transfer",
)
@click.option(
    "--start",
    "-s",
    type=int,
    default="0",
    help="number you want to align to",
)
def main(path, extension,start):
    file_list=listdir(path)
    file_list = [l for l in file_list if l[-len(extension):]==extension]
    file_list.sort()
    path=path+'/'
    
    for i in range(len(file_list)):
        formatted_num = f"{start+i:06d}"+ extension
        rename(path+file_list[i],path+formatted_num) 
    print("MAP ", file_list[0] ," to ", f"{start:06d}"+extension)    
    print("MAP ", file_list[-1] ," to ", f"{start+len(file_list)-1:06d}"+ extension)
        # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if __name__ == "__main__":
    main()