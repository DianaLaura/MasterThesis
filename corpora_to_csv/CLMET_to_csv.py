import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

""""This script transforms files from the CLMET into a .csv-file. 
The goal is to preserve as much information as possible while splitting.

The output is a .csv-file that contains the following attributes 
(derived from XML-tags):

- Sent_ID (generated: sentID_FileID)
- Sent_plain
- Sent_class
- Sent_pos
- File
- File_ID
- Period
- Quartcent
- Decade
- Year
- Genre
- Subgenre
- Title
- Author
- Gender
- Author_birth
- Notes
- Source
- Comments
 """
def get_args():
    parser = argparse.ArgumentParser(description='Parsing arguments like input path, output path, ...')
    parser.add_argument("--input", required=True, type=str, help='Path to input directory')
    parser.add_argument("--output", default='CLMET_data_frame', type=str, help='Path to output directory')
    parser.add_argument ("--sentences", default=False, help= 'variable to enable/disable the tokenization into sentences')
    parser.add_argument("--testing", default=False, help='If set to true, only a small sample of CLMET-documents is processed')

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

    data = pd.DataFrame(columns = ['ID','Text','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
    
    for file in tqdm(os.listdir(plain_docs)):
        
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
            file_title = doc.find('file')
            file_id = doc.find('id')
            period = doc.find('period') 
            quartcent = doc.find('quartcent')
            decade = doc.find('decade')
            year = doc.find('year')
            genre = doc.find('genre')
            subgenre = doc.find('subgenre')
            title = doc.find('title')
            author = doc.find('author')
            gender = doc.find('gender')
            author_birth = doc.find('author_birth')
            notes = doc.find('notes')
            source = doc.find('source')
            comments = doc.find('comments')
            body = doc.find('text')
            text = body.text
        
        except AttributeError:
            error_list.append(file)
            continue
        

        #split text into sentences with NLTK sent_tokenize
        if sentences:
            text = sent_tokenize(text)

            #load sentences and text into pandas data frame

            for sent in range(0,len(text)):
                sent_counter += 1
                sentence= text[sent]
                new_row = pd.DataFrame([[sent_counter, sentence, file_title.text, file_id.text, period.text, quartcent.text, decade.text, year.text, genre.text, subgenre.text, title.text, author.text, gender.text, author_birth.text, notes.text, source.text, comments.text]], columns = ['ID','Text','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
                data = data.append(new_row)
        else:
            sent_counter += 1
            new_row = pd.DataFrame([[sent_counter, text, file_title.text, file_id.text, period.text, quartcent.text, decade.text, year.text, genre.text, subgenre.text, title.text, author.text, gender.text, author_birth.text, notes.text, source.text, comments.text]], columns = ['ID','Text','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
            data = data.append(new_row)
        #condition for finishing during testing
        if testing:
            save_as_csv(data, output_dir, error_list)

    save_as_csv(data, output_dir, error_list)
                







if __name__ == '__main__':
    args = get_args()
    main(args)
