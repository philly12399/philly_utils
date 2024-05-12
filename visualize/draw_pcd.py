import numpy as np
import open3d as o3d
import os

np.set_printoptions(suppress=True) # 取消默认科学计数法，open3d无法读取科学计数法表示
parent = '../data/KITTI_DB/gt_database/0001'
vis = o3d.visualization.Visualizer()
vis.create_window()
for di in sorted(os.listdir(parent)):
    fn = os.path.join(parent,di)
    # 读取点云并可视化
    pcd = np.fromfile(fn, dtype=np.float32).reshape(-1,4)[:,:3] 
    p= o3d.geometry.PointCloud()
    p.points = o3d.utility.Vector3dVector(pcd)
    o3d.visualization.draw_geometries([p,])
    
# p= o3d.geometry.PointCloud()
# p.points = o3d.utility.Vector3dVector(pcd)
# vis = o3d.visualization.Visualizer()

# vis.create_window()
# drawbox(vis,box)
# vis.add_geometry(p)
# # for e in empty_voxel:
# #     drawbox(vis,e)
# vis.get_render_option().background_color = np.asarray([0, 0, 0]) # 設置一些渲染屬性
# vis.run()
# vis.destroy_window()