import json5
import json
import sys
import os
if __name__ == "__main__":

    with open('pcd-detect-kitti.json5', 'r') as file:
        json5_data = file.read()

    data = json5.loads(json5_data)
    seq = sys.argv[1].zfill(4)
    data['pcd_files_dir'] = os.path.join(data['pcd_files_dir'],seq)
    data['output_dir'] = os.path.join(data['output_dir'],seq)
    with open('pcd-detect-kitti-seq.json5', 'w') as file:
        json.dump(data, file, indent=2)