import pandas as pd 
from nltk.tokenize import sent_tokenize , word_tokenize
from tqdm import tqdm

import argparse

"""This script takes a .csv file and a column name, and returns a .csv file in which the specified
column is tokenized."""

def get_args():
    parser = argparse.ArgumentParser(description="Parses Arguments")

    parser.add_argument('--file', required=True, type=str, help='Name of the .csv file that should be tokenized')
    parser.add_argument('--colname', required=True, type=str, help='Name of the column that should be tokenized')
    parser.add_argument('--output_suffix', default='_tokenized', type=str, help='suffix for the name of the output file')
    
    return parser.parse_args()

def main(args):
    file = args.file
    colname = args.colname
    suffix = args.output_suffix

    docs = pd.read_csv(file, sep=';')
  

    print('Tokenizing...')
    for i in tqdm(range(len(docs))):
        text = docs[colname][i]
        sents = sent_tokenize(text)
        tokenized = []
        for sent in range (0, len(sents)):
            tokenized.append(word_tokenize(sents[sent]))
            

        docs[colname][i] = tokenized


    
    print('Save as csv...')
    output_name = file[:-4] + suffix + '.csv'

    docs.to_csv(output_name, sep=';')

    print('Finished!')







if __name__ == '__main__':
    args = get_args()
    main(args)