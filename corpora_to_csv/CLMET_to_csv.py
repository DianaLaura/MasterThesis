import pandas as pd
from bs4 import BeautifulSoup as Soup
import argparse
import os
import re
from nltk.tokenize import sent_tokenize

""""This script splits the CLMET Corpus in a test-, train-, and validation set for performing
data-driven analysis. The goal is to preserve as much information as possible while splitting
the texts of the corpus into sentences.
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
    parser.add_argument("--output", default='clmet_splitted_data', type=str, help='Path to output directory')
    parser.add_argument("--testing", default=False, help='If set to true, only a small sample of CLMET-documents is processed')

    return parser.parse_args()

def save_as_csv(dataframe, output_dir):
    #saves the created data frame as csv and finishes the program. The finishing is here to avoid
    #that the program iterates over more files after completing the test run.

    dataframe.to_csv(output_dir, sep = ';')
    print('Program finished! CSV-File under ' + output_dir)
    exit()

def main(args):
    plain_docs = args.input + "/plain"
    pos_docs = args.input + "/pos"
    output_dir = os.path.join(args.input, args.output) + ".csv"
    pos_available = False

    sent_counter = 0

    data = pd.DataFrame(columns = ['Sent_ID','Sent_plain','Sent_class','Sent_pos','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
    
    for file in os.listdir(plain_docs):
        
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        pos_file = os.fsdecode(os.path.join(pos_docs, file))
        try:
            infile = open(filename)
            doc = Soup(infile.read(), "lxml")
            infile.close()
        except UnicodeDecodeError:
            continue #There are some .DS_store files in this folder

        print('File successfully read!')

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
        plain_body = doc.find('text')
        

        #split text into sentences by using the <p> tag in the corpus

        plain_sents = plain_body.find_all('p')

        print('File tokenized!')

        #load pos file if available
        try:
            infile=open(pos_file)
            pos_doc = Soup(infile.read(),"lxml")
            infile.close

            pos_body = pos_doc.find('text')
            pos_sents = pos_body.find_all('p')

            pos_available = True
        except FileNotFoundError:
            pos_available = False


        #load sentences and text into pandas data frame

        for sent in range(0,len(plain_body)):
            sent_counter += 1
            try:
                sentence= plain_sents[sent].text
            except IndexError:
                break
            if pos_available:
                try:
                    pos_sent = pos_sents[sent].text
                except IndexError:
                    pos_sent = None
            else:
                pos_sent = None

            new_row = pd.DataFrame([[sent_counter, sentence, 'Sent_class', pos_sent, file_title.text, file_id.text, period.text, quartcent.text, decade.text, year.text, genre.text, subgenre.text, title.text, author.text, gender.text, author_birth.text, notes.text, source.text, comments.text]], columns = ['Sent_ID','Sent_plain','Sent_class','Sent_pos','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
            data = data.append(new_row)
            

        print('File loaded into dataframe!')
        #condition for finishing during testing
        if sent_counter >= 1:
            save_as_csv(data, output_dir)

    
                







if __name__ == '__main__':
    args = get_args()
    main(args)
