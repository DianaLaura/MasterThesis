import argparse
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

"""This script takes a .csv file, and creates a stratified test by and
training set. The split is: 80% training set, 20% test set.
For each set, a new file is created with the (optional) name of the corpus and the name of 
the set. A random seed is used to make the split recreatable if the data gets lost.

The strata are ten-year bins, which can be created by using the year of the texts (optional)."""

def get_args():
    parser = argparse.ArgumentParser(description="Parses Arguments like the folder with the document")

    parser.add_argument("--file", required=True, type=str, help="specifies the file that should be splitted")
    parser.add_argument("--seed", default=32, type=int, help="number for the seed that is used for random splitting")
    parser.add_argument("--name", default='', type=str, help="string that is used to create unique names for the output files")
    parser.add_argument("--binning", default=False, help="enables/disables binning into ten-year-periods")
    parser.add_argument("--bin_var", required = True, type=str, help="Takes the name of the column that should be used to create bins or strata")


    return parser.parse_args()

def main(args):

    seed = args.seed
    name = args.name
    file = args.file
    bin_var = args.bin_var
    binning = args.binning

    if name != '':
        name = name + '_'

    train_set = name + "train.csv"
    
    test_set = name + "test.csv"
    
    documents = pd.read_csv(file, sep=';')
    
    #calculate bins
    if binning:
        documents = documents.astype({bin_var:'int16'}, copy=False)
        max_year = documents[bin_var].max()
        while (max_year % 10) != 0:
            max_year +=1
        
        documents['decade'] = str(max_year - (np.trunc((max_year - documents[bin_var])/10) * 10) - 10) + 's'

        bin_var = 'decade'



    train , test = train_test_split(documents, test_size = 0.2, random_state = seed, stratify = documents[bin_var])


    train.to_csv(train_set, sep=';')
    test.to_csv(test_set, sep=';')
    print("All documents: ", len(documents))
    print("Documents in train set: ", len(train))
    print("Documents in test set: ", len(test))


   
    

if __name__ == '__main__':
    args = get_args()
    main(args)