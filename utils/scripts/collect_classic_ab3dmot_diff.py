import os
import sys
import click
import pdb
##AB3DMOT 舊版的RESULT轉成新版的RESULT
@click.command()
### Add your options here
@click.option(
    "--root",
    "-r",
    type=str,
    default="/home/philly12399/thesis/AB3DMOT_backup/tracker_exp_local/BASELINE/age10_cyclist",
    help="Path of detection root .",
)
def main(root):
    diff_range=[0,1,2,3,4]
    
    for diff in diff_range:
        diff_dir=os.path.join(root, f"diff{diff}")
        label_dir=os.path.join(root, f"diff{diff}_val_H1","data_0")
        os.system(f"mkdir {diff_dir} -p")
        os.system(f"cp -r {label_dir} {diff_dir}/label")
        os.system(f"mv {diff_dir}_* {diff_dir}")
        
if __name__ == "__main__":
    main()
