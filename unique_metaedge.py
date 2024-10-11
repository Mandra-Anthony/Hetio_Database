import pandas as pd


def unique_metaedge_values(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t')

    metaedge_column = df['metaedge']

    unique_metaedge_values = metaedge_column.unique()

    print("Unique values in 'metaedge' column:")
    for value in unique_metaedge_values:
        print(value)

unique_metaedge_values('edges.tsv')