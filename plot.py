####OK Plott. Plolttar distanser som motsvaras av avstånd mellan proverna##

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA
from mst_clustering import MSTClustering


nodes='MIC3552A20 MIC3552A21 MIC3552A22 MIC3552A23 MIC3557A53 MIC3557A54 MIC3852A2  MIC4109A21 MIC4461A6  MIC4461A7  MIC4461A8'
nodes=nodes.split()
f=open('dist_the_one_wgs.txt','r')
matrix=[]
row=[]
old_sample=None


for l in f:
    sample,col,w=l.split()
    if old_sample==sample:
        row.append(float(w))
    else:
        if row:
            matrix.append(row)
            row = [float(w)]
        else:
            row.append(float(w))
        old_sample=sample

matrix.append(row)
mat=np.array(matrix)
mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=3,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(mat).embedding_
clf = PCA(n_components=2)
pos = clf.fit_transform(pos)
fig, ax = plt.subplots()

model = MSTClustering(cutoff_scale=200, approximate=False)
labels = model.fit_predict(pos)


#### Om man vill ha kanter:
#X = model.X_fit_
#segments = model.get_graph_segments(full_graph=False)
#ax.plot(segments[0], segments[1], '-k', zorder=1, lw=1)
#ax.scatter(X[:, 0], X[:, 1], c=model.labels_, cmap='rainbow', zorder=2)
#ax.axis('tight')
#####

#### Utan kanter:
plt.scatter(pos[:, 0], pos[:, 1], c=labels, s=100, lw=0)
####

for i, n in enumerate(nodes):
    ax.annotate(n, (pos[i][0],pos[i][1]))

plt.show()




