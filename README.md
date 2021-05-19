# compressMutations
from All mutations to compress table


This program compress monitored_mutations file into compressed table

Input - 
1) monitored_mutations.csv file, the first line MUST be the line of - nucleotide	AA	gene	lineage	type	pos	REF and the samples

![alt text](https://i.gyazo.com/3a007ad068ce12e979c92d5eca1dddfa.png)


2) compressed.csv - this is the template for the compressed output file, any new mutations has to updated here.

![alt text](https://i.gyazo.com/c19557379229248cbc9fd9f806f73171.png)


Output - in the wd -> aftercompress.csv this the compressed file

for example 
python main.py /data3/netanel_scripts/compressMutations/monitored.csv /data3/netanel_scripts/compressMutations/compressed.csv


Notes - 

Sometimes the Mutation Table is changing and that can cause some incompatibility, the compressed.csv template file need to be updated also

If mutation was tracked and than dropped from the mutTable there will be a blank row in the output compressed file. check if this mutation can be deleted from the template file.

If mutation is newly tracking and doesn't appear in the compress template, the name of mutation and lineage will be printed. check if you need to add the mutation to the compressed table template.
