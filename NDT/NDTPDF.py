import numpy as np
from scipy.integrate import tplquad,quad,dblquad
import math
class PDF:
    def __init__(self, mean, cov, voxel_size ,noise=0.05):
        self.mean = mean
        self.cov = cov
        self.cov_inv = np.linalg.pinv(cov)
        self.noise = noise
        self.voxel_size = voxel_size
        self.coef()
        
    # def integrand1(self, x,y,z):
    #     dx = np.array([x,y,z])
    #     exp = np.exp(-0.5*(np.matmul(np.matmul(dx.T, self.cov_inv), dx))) 
    #     return exp

    def coef(self):  
        vs = self.voxel_size
        # xr = (-vs/2,vs/2 )
        # yr = xr
        # zr = xr
        # result,error  = tplquad(self.integrand1, *xr,*yr,*zr)
        # r2 = self.noise*vs**3
        # print(result,error)
        # c2 = 1
        # c1 = (1-r2)/result
        c1 = 10*(1- self.noise)
        c2 = self.noise/(vs**3)
        d3 = -np.log(c2)
        d1 = -np.log(c1 + c2) - d3
        d2 = -2 * np.log((-np.log(c1 * np.exp(-0.5) + c2) - d3) / d1)
        self.d = [0,d1,d2,d3]
        
    def pdf(self, x):  
        x = x.reshape(-1,3)        
        dx = (x - self.mean)
        out=[]
        for i in range(dx.shape[0]):
            factor = 1/np.sqrt(((2*np.pi)**3)*(np.linalg.det(self.cov)))
            exp = np.exp(-0.5*(np.matmul(np.matmul(dx[i].T, self.cov_inv), dx[i])))    
            p = exp*factor
            assert (p != math.inf)  
            # if(p == math.inf):             
            #     p=0          
            out.append(p)
            
        return out

    
    def mixed_pdf(self, x):        
        x = x.reshape(-1,3)
        dx = (x - self.mean)
        out=[]
        c=0
        for i in range(dx.shape[0]):
            p = -self.d[1]*np.exp(-0.5*self.d[2]*np.matmul(np.matmul(dx[i].T, self.cov_inv), dx[i])) 
            assert (p != math.inf)           
            # if(p == math.inf):             
            #     p=0
            out.append(p)        
        return out
 