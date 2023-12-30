import os
import sys
import click
@click.command()
### Add your options here

def main():
    pcd="/home/philly12399/demo_lyft_3d/demo_lyft_3d/LYFT/pointcloud/"
    rep= "/home/philly12399/philly_data/pingtung-tracking-val/val/filtered_seq/seq1/"
    seqlist=sorted(os.listdir(pcd))
    replist=sorted(os.listdir(rep))
    c=5
    for p in seqlist:
        p1=os.path.join(pcd,p)
        p2=os.path.join(rep,replist[c])
        print(p1,p2)
        os.system("cp  {} {}".format(p2, p1))
        c+=1
        
       
        

    
if __name__ == "__main__":
    main()
