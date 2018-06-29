#!/usr/bin/env python

import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from sklearn import manifold
from sklearn.decomposition import PCA
from mst_clustering import MSTClustering

DESC = ''

class DistancePlot():

    def __init__(self, dist_file, classifyer):
        self.dist_file = open(dist_file,'r')
        self.classifyer = float(classifyer)
        self.node_labels = [] 
        self.matrix = []
        self.positions = None    
        self.colors = []

    def make_matrix(self):
        old_sample = None
        row = []
        for line in self.dist_file:
            sample, col, dist = line.split()
            if old_sample == sample:
                row.append(float(dist))
            else:
                if row:
                    self.matrix.append(row)
                    row = [float(dist)]
                else:
                    row.append(float(dist))
                old_sample=sample
                self.node_labels.append(sample)
        self.matrix.append(row)
        self.matrix = np.array(self.matrix)

    def give_2d_positions(self):
        mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=3,
                   dissimilarity="precomputed", n_jobs=1)
        pos = mds.fit(self.matrix).embedding_
        clf = PCA(n_components=2)
        self.positions = clf.fit_transform(pos)

    def cluster(self):
        model = MSTClustering(cutoff_scale = self.classifyer, approximate=False)
        self.colors = model.fit_predict(self.positions)

    def make_plot(self):
        fig, ax = plt.subplots()
        plt.scatter(self.positions[:, 0], self.positions[:, 1], c = self.colors, s=100, lw=0)
        for i, n in enumerate(self.node_labels):
            ax.annotate(n, (self.positions[i][0], self.positions[i][1]))

def main(args):
    DP = DistancePlot(args.dist_file, args.classifyer)
    DP.make_matrix()
    DP.give_2d_positions()
    DP.cluster()
    DP.make_plot()
    plt.show()


if __name__ == "__main__":
    parser = ArgumentParser(description=DESC)
    parser.add_argument('-f', dest='dist_file',
                        help='distance file')
    parser.add_argument('-c', dest='classifyer',
                        help='distance treshold')
    args = parser.parse_args()
    main(args)

