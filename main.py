import pandas as pd
import re
import sys
import numpy as np


def getMutationCompName():
    pass


def main(argv):
    # open the total monitored mutations and the compress mutation tables
    monitored = pd.read_csv(argv[0])
    compress = pd.read_csv(argv[1])
    logfileset={}
    # missing=[]
    # monitored.replace("No Coverage",0,inplace=True)
    # choose tha samples columns from the monitored mutations file
    samplesList = monitored[[col for col in monitored if
                             col.startswith('Env') or col.startswith('nv') or col.startswith('env') or col.startswith(
                                 'p-') or col.startswith(
                                 'P-')]]
    # iterate over each sample from the sample list
    for i, sample in enumerate(samplesList):
        # it = iterator over the mutations in the AA column
        it = enumerate(monitored["AA"])
        # open an empty column with the name of the sample in title
        compress[sample] = ""
        delIndex = 0
        # iterate over mutations per sample
        for index, mutName in it:
            if "B.1.526.1 - New york" in str(monitored.iloc[index]["lineage"]):
                pass
            else:
                try:
                    # Delete mutations
                    if "Deletion" in monitored.iloc[index]["type"] and mutName[0].isupper():
                        # Regex to separate part of the mutation
                        mutRegexed = re.findall('\d+|\D+', mutName)
                        # iterate over all mutations in the compress table to get the index of the desired mutation
                   #     for compi, item in enumerate(compress["Mutation"]):
                   #         itemRegexed = re.findall('\d+|\D+', item)
                   #         if itemRegexed[1] == mutRegexed[1] and itemRegexed[0] == mutRegexed[0]:
                    #            break
                        mutCompressedName = ''.join([i for i in list(compress["Mutation"]) if i.startswith(mutName)])
                        compi = list(compress["Mutation"]).index(mutCompressedName)
                        # the average of the first two nucleotides freq
                        aa = monitored[[sample]].iloc[[index]]
                        ba = monitored[[sample]].iloc[[index + 1]]
                        delMean = monitored[[sample]].iloc[[index, index + 1]].mean(axis=1).values.sum() / 2
                        if delMean != delMean:
                            delMean = "No Coverage"
                        # prev is used to move forward the index in mutations like sgf3xxx-3xxxx
                        else:
                            delIndex = 0
                        # assign the average value in compress index location
                        compress.at[compi, sample] = delMean
                        # skip on the next two nucleotide of the same mutation
                        [next(it, None) for _ in range(2)]
                    elif "Deletion" not in monitored.iloc[index]["type"]:
                        # Point Mutations (only the Non-Synonymous)
                        if re.search("^(?!Synonymous).*$", monitored.iloc[index]["type"]):
                            #for compi, item in enumerate(compress["Mutation"]):
                             #   if mutName in item:
                              #      break
                            mutCompressedName = ''.join([i for i in list(compress["Mutation"]) if i.startswith(mutName)])
                            compi=list(compress["Mutation"]).index(mutCompressedName)
                            valuePerMutation = monitored.iloc[index][sample]
                            compress.at[compi, sample] = valuePerMutation
                # In case of error
                except:
                    logfileset.add("There is no mutation: " + mutName + " in the compressed table, lineage: " +
                          monitored.iloc[index]["lineage"] + "\n":None)
                    # missing.append(mutName)

    # aa=pd.DataFrame(data=set(missing))
    # aa.to_csv("missing.csv")
    f = open("logfile.txt", "w")
    for x in logfileset.keys():
        f.write(x)
    f.close()
    print("compressed table is ready\nLog file is ready")
    compress.to_csv("aftercompress.csv")


if __name__ == '__main__':
    main(sys.argv[1:])
