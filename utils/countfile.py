import os 
p = "/home/philly12399/philly_ssd/KITTI_tracking/training/velodyne/"
dir = sorted(os.listdir(p))
for l in dir:
    thisp=os.path.join(p,l)
    files=sorted(os.listdir(thisp))
    x=int(files[-1][:-4])+1
    print(l,len(files)==x)
# for i in range(2451):
#     p1=os.path.join(p, '02958343_'+str(i))

#     if not os.path.isdir(p1):
#         print(i)
