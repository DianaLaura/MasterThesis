import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

"""
Script that reads meta data from file titles of RIDGES. It will be extended for reading texts, features, etc. later
The following fields are in the output data frame:

- ID
- year
- author (surname)
- title of text

 The output of this script is a .csv-file
"""

def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='RIDGES_DataFrame', type=str, help='Path to output directory')
    parser.add_argument("--sentences", default = False , help='variable to enable/disable the tokenization into sentences')
    parser.add_argument("--testing", default=False, help='If set to true, only a small sample of DTA-documents is processed')


    return parser.parse_args()

def save_as_csv(dataframe, output_dir, error_list):
    #saves the created data frame as csv and finishes the program. The finishing is here to avoid
    #that the program iterates over more files after completing the test run.

    dataframe.to_csv(output_dir, sep = ';')
    print('Program finished! CSV-File under ' + output_dir)
    print('List of files where errors occured:')
    print(error_list)
    exit()


def format_string(string):
    #small function that strips unecessary newlines at the beginning and ending of a string, and transforms multiple lines to
    #one line. The former multiple lines get separated by (',')

    string = string.strip()
    string = re.sub('\n',', ', string)
    string = re.sub('(, )+',', ',string)

    return string

def main(args):
    plain_docs = args.input
    output_dir = os.path.join(args.input, args.output) + ".csv"
    sentences = args.sentences
    testing = args.testing
    sent_counter = 0
    error_list = []

    data = pd.DataFrame(columns = ['ID', 'Year', 'Author', 'Title',])
    
    for file in os.listdir(plain_docs):
        
        """
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        
        try:
            infile = open(filename)
            doc = infile.read()
            infile.close()
        except UnicodeDecodeError:
            error_list.append(file)
            continue #There are some .DS_store files in this folder
        """
        meta = file.split('_')
        
        
        if len(meta) != 3:
            error_list.append(file)
            continue #catch files with titles that are too short or too long
        
        else:
            year = meta[1]
            author = meta[2]
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[0]).strip()
        
        #split text into sentences with NLTK sent_tokenize
        
        
        if sentences:
            #text = sent_tokenize(doc)

        

        

            print('File tokenized!')

            #load sentences and text into pandas data frame
            """
            for sent in range(0,len(text)):
                sent_counter += 1
                sentence = text[sent]
                new_row = pd.DataFrame([[sent_counter, sentence, year, author,title,comment,version]],columns = ['ID', 'Text', 'Year', 'Author', 'Title', 'Comment', 'Version'])
                data = data.append(new_row)"""
        else:
            sent_counter +=1
            new_row = pd.DataFrame([[sent_counter, year, author,title]], columns = ['ID', 'Year', 'Author', 'Title',])
            data = data.append(new_row)

        print(file + ' loaded into dataframe!')

        #condition for finishing during testing
        if testing:
            save_as_csv(data, output_dir, error_list)

    
    save_as_csv(data,output_dir, error_list)
                







if __name__ == '__main__':
    args = get_args()
    main(args)