#using pandas to read tsv files

import pandas as pd

#passing nodes and edges tsv files to 
#read_csv function using a tab separator

nodes_df = pd.read_csv('nodes.tsv', sep='\t')
print(nodes_df)

edges_df = pd.read_csv('edges.tsv', sep='\t')
print(edges_df)
