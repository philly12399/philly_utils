import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import open3d as o3d
class Plot():
    def __init__(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-5, 5)  # Set the x-axis limits
        ax.set_ylim(-5, 5)  # Set the y-axis limits
        ax.set_zlim(-5, 5)  # Set the z-axis limits
        # ax.set_xlim(-20, 20)  # Set the x-axis limits
        # ax.set_ylim(-30, 10)  # Set the y-axis limits
        # ax.set_zlim(-5, 35)  # Set the z-axis limits
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.ax = ax
    def name(self,name):
        plt.title(name)
    def draw_cube(self,vertices):
        s = np.lexsort((vertices[:, 2], vertices[:, 1],vertices[:, 0]))
        vertices = vertices[s]        
       
        # 繪制立方體的六個面
        for i in [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]:
            self.ax.plot([vertices[j][0] for j in i+[i[0]]],
                    [vertices[j][1] for j in i+[i[0]]],
                    [vertices[j][2] for j in i+[i[0]]])
    def draw_bbox_dict(self,bbox): # Object3D
        R = self.roty(bbox['roty'])
        l, w, h = bbox['l'], bbox['w'], bbox['h']
        x = bbox['x']
        y = bbox['y']
        z = bbox['z']
        # 3d bounding box corners
        x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2];
        y_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2];
        z_corners = [h/2,h/2,h/2,h/2,-h/2,-h/2,-h/2,-h/2];
        corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
        corners_3d[0,:] = corners_3d[0,:] + x
        corners_3d[1,:] = corners_3d[1,:] + y
        corners_3d[2,:] = corners_3d[2,:] + z
        corners_3d = np.transpose(corners_3d)
        self.draw_cube(corners_3d)
        return
    
    def draw_bbox_obj(self,bbox): #AB3DMOT OBJ
        R = self.roty(bbox.ry)
        l, w, h = bbox.l, bbox.w, bbox.h
        x = bbox.x
        y = bbox.y
        z = bbox.z
        # 3d bounding box corners
        x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2];
        y_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2];
        z_corners = [h/2,h/2,h/2,h/2,-h/2,-h/2,-h/2,-h/2];
        corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
        corners_3d[0,:] = corners_3d[0,:] + x
        corners_3d[1,:] = corners_3d[1,:] + y
        corners_3d[2,:] = corners_3d[2,:] + z
        corners_3d = np.transpose(corners_3d)
        self.draw_cube(corners_3d)
        return
    
    def draw_point(self,point):
        self.ax.scatter(point[0], point[1], point[2], c='r', marker='o', s=1)
        # 設置坐標軸標簽     
        
    def show1(self):
        plt.show()
        
    def save(self,save_path="./output.png"):
        plt.savefig(save_path)
        
    def roty(self,t):
        """Rotation about the z-axis."""
        c = np.cos(t)
        s = np.sin(t)
        return np.array([[c,  -s,  0],
                        [s,  c,  0],
                        [0, 0,  1]])


def draw_pcd_and_bbox(pcd, box):  
    pcd = pcd[:,:3]
    
    p= o3d.geometry.PointCloud()
    p.points = o3d.utility.Vector3dVector(pcd)
    b = o3d.geometry.OrientedBoundingBox()
    # b.center = [0,0,0]
    b.center = [box['x'],box['y'],box['z']]    
    b.extent = [box['l'],box['w'],box['h']]
    R = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_xyz((0, 0,box['roty']))
    b.rotate(R, b.center)
    
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(p)
    vis.add_geometry(b)
    vis.get_render_option().background_color = np.asarray([0, 0, 0]) # 設置一些渲染屬性
    vis.run()
    vis.destroy_window()
    # o3d.visualization.draw_geometries([p,b], width=800, height=500)    
    return



def draw_pcd_and_bbox_v2(pcd, box):
    l = [make_pcd(pcd),make_bbox(box)]
    draw_all(l)
    return

def make_pcd(pcd):
    pcd = pcd[:,:3] 
    p= o3d.geometry.PointCloud()
    p.points = o3d.utility.Vector3dVector(pcd)
    return p

def make_bbox(box):
    b = o3d.geometry.OrientedBoundingBox()
    # b.center = [0,0,0]    
    b.center = [box['x'],box['y'],box['z']]    
    b.extent = [box['l'],box['w'],box['h']]
    R = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_xyz((0, 0,box['roty']))
    b.rotate(R, b.center)
    return b

def draw_all(l=[]):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    for i in l:
        vis.add_geometry(i)
    vis.get_render_option().background_color = np.asarray([0, 0, 0]) # 設置一些渲染屬性
    vis.run()
    vis.destroy_window()
    return