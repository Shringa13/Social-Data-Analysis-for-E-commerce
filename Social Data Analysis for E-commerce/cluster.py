import sys
import time
import os
import json
import pandas as pd
import math
from collections import defaultdict
from TwitterAPI import TwitterAPI
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import csv


def girvan_newman(G,clust):

    if G.order() == 1:
        return [G.nodes()]
    
    def find_best_edge(G0):
        eb = nx.edge_betweenness_centrality(G0)
        return sorted(eb.items(), key=lambda x: x[1], reverse=True)[0][0]

    components = [c for c in nx.connected_component_subgraphs(G)]

    while len(components) < clust:
        edge_to_remove = find_best_edge(G)

        G.remove_edge(*edge_to_remove)
        components = [c for c in nx.connected_component_subgraphs(G)]

    result = [c.nodes() for c in components]

    return result

	
	
def main():
    G= nx.Graph()
    dfr=pd.read_csv('Followers.csv')
    #print(dfr.values)
    Followers=dfr['follows'].tolist()
    Followers_common=[]
    c= Counter(Followers)
    for userid, count in c.most_common():
        if count>1:
            Followers_common.append(userid)
    df_filtered=dfr.loc[dfr['follows'].isin(Followers_common)]
    for index, row in df_filtered.iterrows():	
        G.add_edge(row['follows'],row['userids'])
    result = girvan_newman(G, 4)
    #print(len(result))
    count=[]
    for r in result:
        count.append(len(r))
    average = sum(count)/len(result)
    prediction = nx.jaccard_coefficient(G)
    w_graph=nx.Graph()
    for u, v, p in prediction:
        #print('(%d, %d) -> %.8f' % (u, v, p))
        w_graph.add_edge(u,v,weight=p)
    nx.draw(w_graph,node_size=50,width=0.25,alpha=0.25,)
    plt.savefig('Graph_Weighted.png')
    with open("Communities.txt", 'w') as outfile:
        outfile.write("%d\n%.2f\n" % (len(result),float(average)))
    	

if __name__ == '__main__':
    main()