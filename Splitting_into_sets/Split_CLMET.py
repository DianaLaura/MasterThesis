import pandas as pd
import xml.etree.ElementTree as et
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
    exit()

def main(args):
    plain_docs = os.fsencode(args.input) #os.fsencode(os.path.join(args.input, "/plain"))
    output_dir = args.output

    sent_counter = 0

    data = pd.DataFrame(columns = ['Sent_ID','Sent_plain','Sent_class','Sent_pos','File','File_ID','Period','Quartcent', 'Decade', 'Year','Genre','Subgenre','Title','Author','Gender','Author_birth','Notes','Source','Comments' ])
    
    for file in os.listdir(plain_docs):
        #extract information from xml
        filename = os.fsdecode(os.path.join(plain_docs,file))
        print("Current file: " + filename)
        
        with open(filename,encoding='utf8') as infile:
            xml = infile.read()
        try:
            doc = et.fromstring("<root>" + xml + "</root>")
            print("File succesfully parsed!")
        except et.ParseError:
            print("Parse Error!")
            continue
        try:
            root = doc.getroot()
        except AttributeError:
            print("Root not found!")
            continue
        file_title = doc.get('file')
        file_id = doc.get('id')
        period = doc.get('period') 
        quartcent = doc.get('quartcent')
        decade = doc.get('decade')
        year = doc.get('year')
        genre = doc.get('genre')
        subgenre = doc.get('subgenre')
        title = doc.get('title')
        author = doc.get('author')
        gender = doc.get('gender')
        author_birth = doc.get('author_birth')
        notes = doc.get('notes')
        source = doc.get('source')
        comments = doc.get('comments')
        text = doc.get('text')

        #split text into sentences with NLTK sent_tokenize

        text = sent_tokenize(text)

        #load sentences and text into pandas data frame

        for sent in range(0,len(text)):
            data.loc[i] = [str(sent)+'_'+ str(file_id)] + text[sent] + 'Sent_class' + 'Sent_pos' + file_title + file_id + period + quartcent + decade + year + genre + subgenre + title + author + gender + author_birth + notes + source + comments
            sent_counter += 1

            if (args.testing==True) and sent_counter == 100:
                save_as_csv(output_dir, data)
                







if __name__ == '__main__':
    args = get_args()
    main(args)
