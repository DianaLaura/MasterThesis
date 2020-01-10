
import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

"""This script splits the DTA Corpus in a test-, train-, and validation set for performing
data-driven analysis. Since the DTA-Corpus provides a lot of information, the features this
program extracts is a pre-selection of all available features from DTA.

The following features are extracted from the DTA-Files:

 - Sentence_ID: generated, unique sentence ID (index of data frame)
 - Sentence
 - Filename
 - DTA_File_ID
 - Title
 - Author
 - Editor_DTA (Editor of version used in the DTA)
 - Edition: Type of the text version (critical, original, etc...)
 - Publisher (of the currently used text)
 - Publication_Year (First Publication)
 - Publication_Place (First Publication)
 - Genre (DTA - Mainclassification)
 - Subgenre (DTA - Subclassification)
 - Notes (Additional information about document)
 - Notes_Edition (Comments about the edition the DTA data is based on)
 - Revision_Remark (Comments about revisisions in the text)
 - Edition_Type (e.g. digital, printed, ...)
 - Editorial_Decl (information about transcription and annotation guidelines)

 DTA-Documentation for TEI-Header (German), 25.12.19: 
 http://www.deutschestextarchiv.de/doku/basisformat/mdUeberblick.html

 The output of this script is a .csv-file
"""

def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='DTA_splitted_data', type=str, help='Path to output directory')
    parser.add_argument("--testing", default=False, help='If set to true, only a small sample of DTA-documents is processed')

    return parser.parse_args()

def save_as_csv(dataframe, output_dir):
    #saves the created data frame as csv and finishes the program. The finishing is here to avoid
    #that the program iterates over more files after completing the test run.

    dataframe.to_csv(output_dir, sep = ';')
    print('Program finished! CSV-File under ' + output_dir)
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

    sent_counter = 0

    data = pd.DataFrame(columns = ['Sent_ID','Sentence','Filename','DTA_File_ID','Title','Author', 'Editor_DTA','Edition','Publisher','Publication_year','Publication_Place','Genre','Subgenre','Notes','Notes_Edition','Revision_Remarks','Edition_type','Editorial_Decl'])
    
    for file in os.listdir(plain_docs):
        
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        
        try:
            infile = open(filename)
            doc = Soup(infile.read(), "lxml")
            infile.close()
        except UnicodeDecodeError:
            continue #There are some .DS_store files in this folder

        print('File successfully read!')

        #extract DTA File id
        file_ids = doc.find('teiheader').find('filedesc').find('publicationstmt').find('idno').findAll('idno')
        for id in file_ids:
            if id['type'] == 'DTAID':
                dta_file_id = id.text
        
        #extract full title
        titles = doc.find('teiheader').find('filedesc').find('titlestmt').findAll('title')
        title = ''
        for item in titles:
            title = title + ' ' + item.text

        author = doc.find('teiheader').find('filedesc').find('titlestmt').find('author').find('persname').text
        author = format_string(author)
        

       

        editors_dta = doc.find('teiheader').find('filedesc').find('titlestmt').findAll('editor')
        editor_dta = ''
        for person in editors_dta:
            current_person = person.text
            current_person = format_string(current_person)
            editor_dta += current_person + '\n'
        
        edition = doc.find('teiheader').find('filedesc').find('editionstmt').find('edition').text

        publisher = doc.find('teiheader').find('filedesc').find('titlestmt').find('respstmt').text
        publisher = format_string(publisher)
        
        pub_years = doc.find('teiheader').find('filedesc').find('sourcedesc').find('biblfull').find('publicationstmt').findAll('date')
        
        
        for id in pub_years:
            if (id['type'] == 'firstPublication') and (id != None):
                #sometimes, there is a separate date for the first publication given, but not always
                publication_year = id.text

            elif (id['type'] == 'publication'):
                publication_year = id.text
    
        
        publication_place = doc.find('teiheader').find('filedesc').find('sourcedesc').find('biblfull').find('publicationstmt').find('pubplace').text

        all_genres = doc.find('teiheader').find('profiledesc').find('textclass').findAll('classcode')
        
        for id in all_genres:
            if id['scheme'] == 'http://www.deutschestextarchiv.de/doku/klassifikation#dtamain':
                genre = id.text
            if id['scheme'] == 'http://www.deutschestextarchiv.de/doku/klassifikation#dtasub':
                subgenre = id.text
        
        notes = doc.find('teiheader').find('filedesc').find('notesstmt')

        if notes != None:
            notes = notes.find('note').text
        
        else:
            notes = '-'
        

        notes_edition = doc.find('teiheader').find('filedesc').find('sourcedesc').find('notesstmt')

        if notes_edition != None:
            notes_edition = notes_edition.find('note').text

        else:
            notes_edition = '-'
       
        revision_remarks = doc.find('teiheader').find('filedesc').find('respstmt').find('resp').findAll('note')


        print(revision_remarks)

        




        

        #split text into sentences with NLTK sent_tokenize

        #text = sent_tokenize(text)

        

        

        print('File tokenized!')

        #load sentences and text into pandas data frame

        for sent in range(0,10):#len(text)):
            sent_counter += 1
            #sentence = text[sent]
            new_row = pd.DataFrame([[sent_counter,'sentence',file, dta_file_id,title, author, editor_dta, edition, publisher, publication_year, publication_place,genre,subgenre, notes, notes_edition, 'Revision_Remarks','Edition_type','Editorial_Decl']],columns = ['Sent_ID','Sentence','Filename','DTA_File_ID','Title','Author', 'Editor_DTA','Edition','Publisher','Publication_year','Publication_Place','Genre','Subgenre','Notes','Notes_Edition','Revision_Remarks','Edition_type','Editorial_Decl'])
            data = data.append(new_row)
            

        print('File loaded into dataframe!')
        #condition for finishing during testing
        if sent_counter >= 1:
            save_as_csv(data, output_dir)

    
                







if __name__ == '__main__':
    args = get_args()
    main(args)