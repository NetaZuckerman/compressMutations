import pandas as pd
import re


def getMutationCompName():
    pass


def main():
    # open the total monitored mutations and the compress mutation tables
    monitored = pd.read_csv("monitored.csv")
    compress = pd.read_csv("compressed.csv")
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
        # iterate over mutations per sample
        for index, mutName in it:
            try:
                # Delete mutations
                if "Deletion" in monitored.iloc[index]["type"]:
                    mutRegexed = re.findall('\d+|\D+', mutName)
                    if "-" in mutRegexed:
                        [next(it, None) for _ in range(2)]
                    else:
                        for compi, item in enumerate(compress["Mutation"]):
                            itemRegexed = re.findall('\d+|\D+', item)
                            if itemRegexed[1] == mutRegexed[1]:
                                break
                        delMean = monitored[[sample]].iloc[[index, index + 1]].mean(axis=0).values
                        compress.at[compi, sample] = float(delMean)
                else:
                    # Point Mutations (only the Non-Synonymous)
                    if re.search("^(?!Synonymous).*$", monitored.iloc[index]["type"]):
                        for compi, item in enumerate(compress["Mutation"]):
                            if mutName in item:
                                break
                        valuePerMutation = monitored.iloc[index][sample]
                        compress.at[compi, sample] = valuePerMutation
            # In case of error
            except:
                print("index: " + str(index) + " is empty\n")
    compress.to_csv("newc.csv")


if __name__ == '__main__':
    main()
