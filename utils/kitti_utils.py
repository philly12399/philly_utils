import numpy as np
from kitti_calib import Calibration
import copy
import pdb
def get_calib_from_file(calib_file):
    return Calibration(calib_file)
    
def get_objects_from_label(label_file, mode, calib, dataset):
    with open(label_file, 'r') as f:
        lines = f.readlines()
    objects = [Object3d(line, mode, calib, dataset) for line in lines]
    return objects

class Object3d(object):
    def __init__(self, line, mode, calib, dataset):
        label = line.strip().split(' ')
        self.src = line
        self.dataset = dataset.lower()
        if(mode == "track"):
            self.frame_id = int(label[0])
            self.track_id = int(label[1])
            label = label[2:]
        self.obj_type = label[0].lower()
        self.truncation = float(label[1])
        self.occlusion = int(label[2])  # 0:fully visible 1:partly occluded 2:largely occluded 3:unknown
        self.alpha = float(label[3])
        self.box2d = {'x1': float(label[4]), 'y1': float(label[5]), 'x2': float(label[6]), 'y2': float(label[7])}
        self.box3d = {'h': float(label[8]), 'w': float(label[9]), 'l': float(label[10]),\
            'x':float(label[11]) ,'y':float(label[12]) ,'z':float(label[13]) , 'roty': float(label[14])}
        if(self.dataset == "kitti"): #rect to velo
            self.box3d = bbox_rect_to_velo(self.box3d, calib)
        elif(self.dataset == "wayside"): #H,L互換
            self.box3d['h'] ,self.box3d['w'] ,self.box3d['l'] = self.box3d['l'] ,self.box3d['w'] ,self.box3d['h'] 
            pass
        else: assert False
        self.score = float(label[15]) if label.__len__() == 16 else -1.0

    def to_str(self):
        # print_str = f"{self.obj_type} {self.truncation} {self.occlusion} {self.alpha} box2d: {self.box2d} box3d: {self.box3d} score:{self.score }"
        print_str = f"{self.obj_type} box3d: {self.box3d} score:{self.score }"
        
        return print_str
import plot
import math
import pdb

def points_in_box(points, bbox):
    center = np.array([bbox['x'], bbox['y'], bbox['z']])
    R = rotz(-bbox['roty'])
    # move to origin and rotate and move back
    rot_points = np.dot(R, (points-center).T).T+center
    in_points_flag = in_bbox(rot_points, bbox)
    return in_points_flag

def bbox_rect_to_velo(bbox, calib):
    center = np.array([bbox['x'], bbox['y'], bbox['z']])
    center = calib.project_rect_to_velo(center.reshape(1,3)).reshape(3)
    roty = calib.rect_to_velo_rot(bbox['roty'])
    
    bbox_velo = copy.copy(bbox)
    bbox_velo['x'], bbox_velo['y'], bbox_velo['z'], bbox_velo['roty'] = center[0],center[1],center[2],roty
    bbox_velo['z'] += bbox_velo['h']/2
    return bbox_velo
    
def in_bbox(points, bbox):
    bbox_rotz(bbox) # find 8 edge of bbox
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


def bbox_rotz(bbox): # find 8 edge of bbox
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