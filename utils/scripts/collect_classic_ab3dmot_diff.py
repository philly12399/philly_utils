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
    default="",
    help="Path of detection root .",
)
#root="/home/philly12399/thesis/AB3DMOT/tracker_exp_local/0612_KT_BASELINE"
def main(root):
    # root="/home/philly12399/thesis/AB3DMOT/tracker_exp_local/Wayside40"
    diff_range=[0,1,2,3,4]
    for r1 in sorted(os.listdir(root)):
        r1 = os.path.join(root, r1)
        for diff in diff_range:
            diff_dir=os.path.join(r1, f"diff{diff}")
            label_dir=os.path.join(r1, f"diff{diff}_val_H1","data_0")
            os.system(f"mkdir {diff_dir} -p")
            os.system(f"cp -r {label_dir} {diff_dir}/label")
            os.system(f"mv {diff_dir}_* {diff_dir}")
            
if __name__ == "__main__":
    main()
