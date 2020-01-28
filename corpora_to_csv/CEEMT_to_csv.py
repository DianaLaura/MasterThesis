import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

"""This script reads files from a folder with EMEMT or LMEMT into a .csv data frame.
The text can optionally be splitted into sentences, the default setting is to 
extract just the document.

The EMEMT and LMEMT files do not provide meta data in a reliable way inside of their files.
The meta data is extracted from the title of the file.

The following fields are in the output data frame:

- ID
- Text (full text or single sentence)
- year
- author (surname)
- title of text
- comment (0 = no, 1 = yes)
- version (e.g. shortened, first proof, etc.)

There are some files in the EMEMT that are extracted from a journal named "Philosophical Transactions".

The author of these files is pt + a number, e.g. pt1. The title are the page numbers from the file, e.g.
23-27.

 The output of this script is a .csv-file
"""

def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='CEEMT_DataFrame', type=str, help='Path to output directory')
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

    data = pd.DataFrame(columns = ['ID', 'Text', 'Year', 'Author', 'Title', 'Comment', 'Version'])
    
    for file in os.listdir(plain_docs):
        
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        
        try:
            infile = open(filename)
            doc = infile.read()
            infile.close()
        except UnicodeDecodeError:
            error_list.append(file)
            continue #There are some .DS_store files in this folder

        meta = file[:-4].split('_')
        
        
        if (len(meta) < 3) or len(meta) > 6:
            error_list.append(file)
            continue #catch files with titles that are too short or too long for being from CEEMT 
        
        elif len(meta) == 3:
            year = meta[0]
            author = 'anonymous'
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[1]).strip()
            comment = 0
            version = meta[2]
        
        elif (len(meta)) == 4 and (meta[2] == 'comment' or meta[2]=='comments'):
            year = meta[0]
            author = 'anonymous'
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[1]).strip()
            comment = 1
            version = meta[3]

        elif (len(meta)) == 4:
            year = meta[0]
            author = meta[1]
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[2]).strip()
            comment = 0
            version = meta[3]

        elif (len(meta)) == 5 and (meta[3] == 'comment' or meta[3] == 'comments'):
            year = meta[0]
            author = meta[1]
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[2]).strip()
            comment = 1
            version = meta[4]
        
        elif (len(meta)) == 5:
            year = meta[0]
            author = meta[1]
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[2]).strip()
            comment = 0
            version = meta[3] + ',' + ' ' + meta[4]
        
        elif (len(meta) == 6 and (meta[3] == 'comment' or meta[3] == 'comments')):
            year = meta[0]
            author = meta[1]
            title = re.sub('(?=[A-Z])(?=[A-Z])',' ',meta[2]).strip()
            comment = 1
            version = meta[4] + ',' + ' ' + meta[5]
        else:
            error_list.append(file)
            continue
        #split text into sentences with NLTK sent_tokenize
        

        if sentences:
            text = sent_tokenize(doc)

        

        

            print('File tokenized!')

            #load sentences and text into pandas data frame

            for sent in range(0,len(text)):
                sent_counter += 1
                sentence = text[sent]
                new_row = pd.DataFrame([[sent_counter, sentence, year, author,title,comment,version]],columns = ['ID', 'Text', 'Year', 'Author', 'Title', 'Comment', 'Version'])
                data = data.append(new_row)
        else:
            sent_counter +=1
            new_row = pd.DataFrame([[sent_counter, doc, year, author,title, comment,version]], columns = ['ID', 'Text', 'Year', 'Author', 'Title', 'Comment', 'Version'])
            data = data.append(new_row)

        print(file + ' loaded into dataframe!')

        #condition for finishing during testing
        if testing:
            save_as_csv(data, output_dir, error_list)

    
    save_as_csv(data,output_dir, error_list)
                







if __name__ == '__main__':
    args = get_args()
    main(args)