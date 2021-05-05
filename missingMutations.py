import pandas as pd
import sys

missing = pd.read_csv("missing.csv")
mutable = pd.read_csv("novelMutTable.csv")
lineage = []
gene = []

for i in range(len(missing)):
    lineage.append((mutable[(mutable['AA'] == missing['0'][i])]["lineage"].values).astype(str))
    gene.append((mutable[(mutable['AA'] == missing['0'][i])]["gene"].values))

missing['lineage'] = lineage
missing['gene'] = gene

missing['total'] = missing['0'].astype(str).map(lambda x: x.lstrip('[').rstrip(']')) +" ("+ missing['gene'].astype(str).map(lambda x: x.lstrip("['").rstrip("']"))+")"


missing.to_csv("missing2.csv")
