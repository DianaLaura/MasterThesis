import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

"""This script reads files from a folder with ARCHER-files into a .csv data frame.
The text can optionally be splitted into sentences, the default setting is to 
extract just the document.

The following features are extracted from the ARCHER-Files (additionally to the text):

 - ID: generated, unique ID (index of data frame)
 - Text / Sentence
 - Filename
 - Title
 - Author
 - Sex (of author)
 - Year
 - Period
 - Genre
 - Lang_variety
 - Notes (Additional information about document)
 - Editorial_Decl (information about transcription and annotation guidelines)

 The output of this script is a .csv-file
"""

def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='ARCHER_data_frame', type=str, help='Path to output directory')
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

    data = pd.DataFrame(columns = ['ID','Text','Filename','Title','Author', 'Sex', 'Year','Period','Lang_variety','Genre','Notes', 'Editorial_Decl'])
    
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

        try:
            
            author = doc.find('teiheader').find('filedesc').find('titlestmt').find('author').text

            sex = doc.find('teiheader').find('filedesc').find('titlestmt').find('sex').text

            title = doc.find('teiheader').find('filedesc').find('sourcestmt').find('bibl').find('p').text

            year = doc.find('teiheader').find('filedesc').find('sourcestmt').find('bibl').find('date').text 

            
            taxonomy = doc.find('teiheader').find('classdecl').findAll('taxonomy')

            genre = ''
            period = ''
            lang_variety = ''

            for item in taxonomy:
                if item['type'] == 'Genre':
                    genre = item.find('category').find('catdesc').text
                
                elif item['type'] == 'Period':
                    period = item.find('category').find('catdesc').text
                
                elif item['type'] == 'Variety':
                    lang_variety = item.find('category').find('catdesc').text
                
          

            notes = doc.find('teiheader').find('filedesc').find('notesstmt')

            if notes != None:
            
                notes = format_string(notes.text)
            else:
                notes = '-'

            editorial_decl = doc.find('teiheader').find('encodingdesc').find('editorialdecl')

            if editorial_decl != None:
                editorial_decl = format_string(editorial_decl.text)
            else:
                editorial_decl = '-'
        except AttributeError:
            print('Error: Could not find all attributes in the file' + file)
            error_list.append(file)
            continue

        #split text into sentences with NLTK sent_tokenize
        header = doc.find('body').find('text').find('teiheader').text


        text = doc.find('body').text

        text = text[len(header):]



        if sentences:
            text = sent_tokenize(text)
        

            print('File tokenized!')

            #load sentences and text into pandas data frame

            for sent in range(0,len(text)):
                sent_counter += 1
                sentence = text[sent]
                new_row = pd.DataFrame([[sent_counter,sentence,file,title, author, sex, year, period, lang_variety, genre, notes, editorial_decl]], columns = ['ID','Text','Filename','Title','Author', 'Sex', 'Year','Period','Lang_variety','Genre','Notes', 'Editorial_Decl'])
                data = data.append(new_row)
        else:
            sent_counter +=1
            new_row = pd.DataFrame([[sent_counter,text,file,title, author, sex, year, period, lang_variety, genre, notes, editorial_decl]], columns = ['ID','Text','Filename','Title','Author', 'Sex', 'Year','Period','Lang_variety','Genre','Notes', 'Editorial_Decl'])
            data = data.append(new_row)

        print(file + ' loaded into dataframe!')

        #condition for finishing during testing
        if testing:
            save_as_csv(data, output_dir, error_list)

    
    save_as_csv(data,output_dir, error_list)
                







if __name__ == '__main__':
    args = get_args()
    main(args)