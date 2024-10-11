#using pandas to read tsv files

import pandas as pd

#passing nodes and edges tsv files to 
#read_csv function using a tab separator

nodes_df = pd.read_csv('Data/nodes.tsv', sep='\t')
edges_df = pd.read_csv('Data/edges.tsv', sep='\t')

