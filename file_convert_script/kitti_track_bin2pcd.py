import os
import bin_2_pcd  
#把kitti track的velodyne(bin)轉pcd的腳本
if __name__ == "__main__":
    kitti_root = "../data/KITTI_tracking/training/velodyne/"
    out_root =  "../data/KITTI_tracking/training/seqpcd/"
    for seq in sorted(os.listdir(kitti_root)):
        seq_path = os.path.join(kitti_root, seq)
        out_path = os.path.join(out_root, seq)
        os.system(f"mkdir -p {out_path}")
        print(f"convert {seq_path} to {out_path}")
        bin_2_pcd.convert(seq_path, out_path ,-1)