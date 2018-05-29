
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

nodes='MIC3551A7 MIC3558A2 MIC4109A19 MIC4109A20 MIC4202A34 MIC4202A36 MIC4202A37 MIC4202A39 MIC4353A1'

labels={'MIC3558A2':'18ET500006',
'MIC4202A39':'18ET500069',
'MIC4202A36':'18ET500066',
'MIC4202A37':'18ET500067',
'MIC4202A34':'18ET500064',
'MIC4109A20':'18ET500045',
'MIC4353A1':'18ET500070',
'MIC4109A19':'18ET500044',
'MIC3551A7':'17ET500074'}

nodes=nodes.split()

f=open('dist.txt','r')
#f=open('high_cov_dist.txt','r')
G=nx.Graph()
G.add_nodes_from(nodes)
we=[]
for line in f:
    a,b,c=line.split()
    G.add_edge(a,b,weight=c, label=c)

T=nx.minimum_spanning_tree(G)
edge_labels = nx.get_edge_attributes(T,'label')
pos = nx.spring_layout(T,scale=2)
nx.draw(T,pos )#,with_labels = True)
nx.draw_networkx_labels(T, pos, labels=labels)
nx.draw_networkx_edge_labels(T, pos, edge_labels=edge_labels)
plt.show()


