import pandas as pd
import re
import sys


def getMutationCompName():
    pass


def main(argv):
    # open the total monitored mutations and the compress mutation tables
    monitored = pd.read_csv(argv[0])
    compress = pd.read_csv(argv[1])
    # choose tha samples columns from the monitored mutations file
    samplesList = monitored[[col for col in monitored if
                             col.startswith('Env') or col.startswith('nv') or col.startswith('p-') or col.startswith(
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
            if mutName == "27338Del":
                pass

            else:
                try:
                    if mutName == 'D215G':
                        a = 3
                    # Delete mutations
                    if "Deletion" in monitored.iloc[index]["type"]:
                        # Regex to separate part of the mutation
                        mutRegexed = re.findall('\d+|\D+', mutName)
                        # iterate over all mutations in the compress table to get the index of the desired mutation
                        for compi, item in enumerate(compress["Mutation"]):
                            itemRegexed = re.findall('\d+|\D+', item)
                            if itemRegexed[1] == mutRegexed[1]:
                                break
                        # the average of the first two nucleotides freq
                        delMean = monitored[[sample]].iloc[[index, index + 1]].mean(axis=0).values
                        # prev is used to move forward the index in mutations like sgf3xxx-3xxxx
                        if mutName == prev:
                            delIndex += 1
                            compi += delIndex
                        else:
                            delIndex = 0
                        # assign the average value in compress index location
                        compress.at[compi, sample] = float(delMean)
                        # skip on the next two nucleotide of the same mutation
                        [next(it, None) for _ in range(2)]
                    else:
                        # Point Mutations (only the Non-Synonymous)
                        if re.search("^(?!Synonymous).*$", monitored.iloc[index]["type"]):
                            for compi, item in enumerate(compress["Mutation"]):
                                if mutName in item:
                                    break
                            valuePerMutation = monitored.iloc[index][sample]
                            compress.at[compi, sample] = valuePerMutation
                    prev = mutName
                # In case of error
                except:
                    print("index: " + str(index) + " is empty\n")
    compress.to_csv("aftercompress.csv")


if __name__ == '__main__':
    main(sys.argv[1:])
