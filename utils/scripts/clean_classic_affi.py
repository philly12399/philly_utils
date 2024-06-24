import os
import sys
import click
import pdb
##AB3DMOT 舊版的RESULT轉成新版的RESULT
@click.command()
### Add your options here
@click.option(
    "--allroot",
    "-r",
    type=str,
    default="",
    help="Path of detection root .",
)
def main(allroot):
    # allroot="/home/philly12399/thesis/AB3DMOT/tracker_exp_local/Wayside40/"    
    
    diff_range=[0,1,2,3,4]    
    
    for root in os.listdir(allroot):
        root = os.path.join(allroot, root)
        for rootl2 in os.listdir(root):
            rootl2 = os.path.join(root, rootl2)
            os.system(f"rm -rf {rootl2}/affi*")
            os.system(f"rm -rf {rootl2}/vis_debug")
            os.system(f"rm -rf {rootl2}/combine_log.txt")
  
if __name__ == "__main__":
    main()
