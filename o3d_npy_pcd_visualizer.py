import numpy as np
import open3d as o3d
import os

np.set_printoptions(suppress=True) # 取消默认科学计数法，open3d无法读取科学计数法表示
parent = './data/shape'
for di in os.listdir(parent):
    fn = f'{parent}/{di[:-4]}'

    data = np.load(f'{fn}.npy')
    np.savetxt(f'{fn}.txt', data)
    # 读取点云并可视化
    pcd =o3d.io.read_point_cloud(f'{fn}.txt', format='xyz') # 原npy文件中的数据正好是按x y z r g b进行排列
    print(pcd)
    o3d.visualization.draw_geometries([pcd], width=1200, height=600)
    os.remove(f'{fn}.txt')
    
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