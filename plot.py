import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class Plot():
    def __init__(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-5, 5)  # Set the x-axis limits
        ax.set_ylim(-5, 5)  # Set the y-axis limits
        ax.set_zlim(-5, 5)  # Set the z-axis limits
        # ax.set_xlim(-20, 40)  # Set the x-axis limits
        # ax.set_ylim(-30, 30)  # Set the y-axis limits
        # ax.set_zlim(-5, 55)  # Set the z-axis limits
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
    def draw_point(self,point):
        self.ax.scatter(point[0], point[1], point[2], c='r', marker='o', s=1)
        # 設置坐標軸標簽     
    def show(self):
        plt.show()


# cube_vertices = np.array([
#     [0, 0, 0],
#     [1, 0, 0],
#     [0, 1, 0],
#     [1, 1, 0],
#     [0, 0, 1],
#     [1, 0, 1],
#     [0, 1, 1],
#     [1, 1, 1]
# ])
