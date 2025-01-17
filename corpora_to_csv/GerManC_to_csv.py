import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

"""This script reads files from a folder with GerManC files in the TEI-XML format into a .csv data frame.
The text can optionally be splitted into sentences, the default setting is to 
extract just the document.

The following features are extracted from the files (additionally to the text):

 - ID: generated, unique ID (index of data frame)
 - Sentence / Text
 - Filename
 - Author (for genres that do not provide the author, this field is filled in with 'unknown')
 - Title
 - Genre
 - Year (of publication)
 - Period (50-year periods as specified by the editors of GerManC)
 - Region (where the text was written)

 The output of this script is a .csv-file
"""

def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='GerManc_data_frame', type=str, help='Path to output directory')
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

    data = pd.DataFrame(columns = ['ID','Text','Filename','Title','Author','Genre','Year','Period','Region'])
    
    for file in os.listdir(plain_docs):
        
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        
        try:
            infile = open(filename)
            doc = Soup(infile.read(), "lxml")
            infile.close()
        except UnicodeDecodeError:
            error_list.append(file)
            continue


        try: #special exception because NEWS-files do not provide a tag 'author'
            author = doc.find('teiheader').find('titlestmt').find('author').text
        except AttributeError:
            author = 'unknown'

        try:
            
            title = doc.find('teiheader').find('filedesc').find('titlestmt').find('title').text
            
            year = doc.find('teiheader').find('filedesc').find('publicationstmt').find('date').text

            notes = doc.find('teiheader').find('filedesc').find('notesstmt').findAll('note')

            genre = 'unknown'
            period = 'unknown'
            region = 'unknown'
            for item in notes:
                if item['type'] == 'region':
                    region = item.text
                elif item['type'] == 'genre':
                    genre = item.text
                
                elif item['type'] == 'period':
                    period = item.text
        except AttributeError:
            print('Error: Could not find all attributes in the file' + file)
            error_list.append(file)
            continue

        #split text into sentences with NLTK sent_tokenize
        body = doc.find('text').text

        if sentences:
            text = sent_tokenize(body)

        

        

            print('File tokenized!')

            #load sentences and text into pandas data frame

            for sent in range(0,len(text)):
                sent_counter += 1
                sentence = text[sent]
                new_row = pd.DataFrame([[sent_counter,sentence,file,title, author, genre,year,period,region]],columns = ['ID','Text','Filename','Title','Author','Genre','Year','Period','Region'])
                data = data.append(new_row)
        else:
            sent_counter +=1
            new_row = pd.DataFrame([[sent_counter,body,file,title,author,genre,year,period,region]],columns = ['ID','Text','Filename','Title','Author','Genre','Year','Period','Region'])
            data = data.append(new_row)

        print(file + ' loaded into dataframe!')

        #condition for finishing during testing
        if testing:
            save_as_csv(data, output_dir, error_list)

    
    save_as_csv(data,output_dir, error_list)
                







if __name__ == '__main__':
    args = get_args()
    main(args)