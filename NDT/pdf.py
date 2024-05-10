import scipy
import numpy as np
def pdf(x, mean, cov):
    # 計算協方差矩陣的逆矩陣
    cov_inv = np.linalg.pinv(cov)    
    # 計算偏差向量
    dx = (x - mean)


    # Mahalanobis 距離的平方
    factor = 1/np.sqrt(((2*np.pi)**3)*(np.linalg.det(cov)))
    exp = np.exp(-0.5*(np.matmul(np.matmul(dx.T, cov_inv), dx)))
    pdf = exp * factor
    print(pdf)
    # 多變量正態分佈的概率密度函數
    
    return pdf

np.random.seed(0)


v={'mean':[-2.11875071, -0.66622021, -0.24961332],'cov':[[ 0.01757985, -0.01172799, -0.00651389] ,[-0.01172799,  0.01646898,  0.00714759],[-0.00651389,  0.00714759,  0.00809525]]}
v={'mean':[0,0,0],'cov':[[ 1,0,0] ,[0,1,0],[0,0,1]]}

scalar=1
v['mean'] = np.array(v['mean'])*scalar
v['cov'] = np.array(v['cov'])*scalar*scalar

samples = np.random.multivariate_normal(v['mean'], v['cov'], 10)

# mvn = scipy.stats.multivariate_normal(mean=v['mean'], cov=v['cov'], allow_singular=True)

# print(mvn.pdf(samples[0]))
pdf(v['mean'], v['mean'], v['cov'])


