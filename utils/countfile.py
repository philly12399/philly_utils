import os 
p = "/home/philly12399/philly_data/point_mae/output/rand_0.9_occall/"
for i in range(2451):
    p1=os.path.join(p, '02958343_'+str(i))

    if not os.path.isdir(p1):
        print(i)
