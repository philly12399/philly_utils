import os
import sys

import pdb
##AB3DMOT 舊版的RESULT轉成新版的RESULT

def main():
    allroot="/home/philly12399/thesis/AB3DMOT_backup/tracker_exp_local/BASELINE/"
    diff_range=[0,1,2,3,4]    
    
    for root in os.listdir(allroot):
        root = os.path.join(allroot, root)
        for diff in diff_range:
            diff_dir=os.path.join(root, f"diff{diff}")
            # os.system(f"rm -rf {diff_dir}/label/data_0")
        
if __name__ == "__main__":
    main()
