import numpy as np
def get_calib_from_file(calib_file):
    with open(calib_file) as f:
        lines = f.readlines()

    obj = lines[2].strip().split(' ')[1:]
    P2 = np.array(obj, dtype=np.float32)
    obj = lines[3].strip().split(' ')[1:]
    P3 = np.array(obj, dtype=np.float32)
    obj = lines[4].strip().split(' ')[1:]
    R0 = np.array(obj, dtype=np.float32)
    obj = lines[5].strip().split(' ')[1:]
    Tr_velo_to_cam = np.array(obj, dtype=np.float32)

    return {'P2': P2.reshape(3, 4),
            'P3': P3.reshape(3, 4),
            'R0': R0.reshape(3, 3),
            'Tr_velo2cam': Tr_velo_to_cam.reshape(3, 4)}
    
def get_objects_from_label(label_file):
    with open(label_file, 'r') as f:
        lines = f.readlines()
    objects = [Object3d(line) for line in lines]
    return objects

class Object3d(object):
    def __init__(self, line):
        label = line.strip().split(' ')
        self.src = line
        self.obj_type = label[0].lower()
        # self.cls_id = cls_type_to_id(self.cls_type)
        self.truncation = float(label[1])
        self.occlusion = int(label[2])  # 0:fully visible 1:partly occluded 2:largely occluded 3:unknown
        self.alpha = float(label[3])
        self.box2d = {'x1': float(label[4]), 'y1': float(label[5]), 'x2': float(label[6]), 'y2': float(label[7])}
        self.box3d = {'h': float(label[10]), 'w': float(label[9]), 'l': float(label[8]),\
            'x':float(label[11]) ,'y':float(label[12]) ,'z':float(label[13]) , 'roty': float(label[14])}
        # self.dis_to_cam = np.linalg.norm(self.loc)
        self.score = float(label[15]) if label.__len__() == 16 else -1.0
        # self.level_str = None
        # self.level = self.get_kitti_obj_level()
    def to_str(self):
        # print_str = f"{self.obj_type} {self.truncation} {self.occlusion} {self.alpha} box2d: {self.box2d} box3d: {self.box3d} score:{self.score }"
        print_str = f"{self.obj_type} box3d: {self.box3d} score:{self.score }"
        
        return print_str
import plot
import math

def points_in_box(points, bbox):
    bbox_rotz(bbox)
    center = np.array([bbox['x'], bbox['y'], bbox['z']])
    R = rotz(-bbox['roty'])
    # move to origin and rotate and move back
    rot_points = np.dot(R, (points-center).T).T+center
    in_points_flag = in_bbox(rot_points, bbox)
    return in_points_flag

def in_bbox(points, bbox):
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    x_min = bbox['x'] - bbox['l'] / 2
    x_max = bbox['x'] + bbox['l'] / 2
    y_min = bbox['y'] - bbox['w'] / 2
    y_max = bbox['y'] + bbox['w'] / 2
    z_min = bbox['z'] - bbox['h'] / 2
    z_max = bbox['z'] + bbox['h'] / 2
    return (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max) & (z >= z_min) & (z <= z_max)


def bbox_rotz(bbox):
    R = rotz(bbox['roty'])
    l, w, h = bbox['l'], bbox['w'], bbox['h']
    # 3d bounding box corners
    x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2];
    y_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2];
    z_corners = [h/2,h/2,h/2,h/2,-h/2,-h/2,-h/2,-h/2];

    # origin  cube vertex
    corners_3d0 = np.vstack([x_corners, y_corners, z_corners])
    corners_3d0[0,:] = corners_3d0[0,:] + bbox['x']
    corners_3d0[1,:] = corners_3d0[1,:] + bbox['y']
    corners_3d0[2,:] = corners_3d0[2,:] + bbox['z']
    corners_3d0 = np.transpose(corners_3d0)
    bbox['corners_org'] = corners_3d0
    
    # rotated  cube vertex
    corners_3d = np.dot(R, np.vstack([x_corners, y_corners, z_corners]))
    corners_3d[0,:] = corners_3d[0,:] + bbox['x']
    corners_3d[1,:] = corners_3d[1,:] + bbox['y']
    corners_3d[2,:] = corners_3d[2,:] + bbox['z']
    corners_3d = np.transpose(corners_3d)
    bbox['corners_3d_cam'] = corners_3d
    
    return corners_3d

def rotz(t):
    """Rotation about the z-axis."""
    c = np.cos(t)
    s = np.sin(t)
    return np.array([[c,  -s,  0],
                     [s,  c,  0],
                     [0, 0,  1]])