import argparse
import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split

"""This script takes a folder full of documents, and creates a test, validation and
training set. The split is: 80% training set, 10% validation set, 10% test set.
For each set, a new folder is created with the (optional) name of the corpus and the name of 
the set. A random seed is used to make the split recreatable if the data gets lost."""

def get_args():
    parser = argparse.ArgumentParser(description="Parses Arguments like the folder with the document")

    parser.add_argument("--folder", required=True, type=str, help="specifies the folder that contains the documents for splitting")
    parser.add_argument("--seed", default=32, type=int, help="number for the seed that is used for random splitting")
    parser.add_argument("--name", default='', type=str, help="string that is used to create unique names for the output folders")

    return parser.parse_args()

def main(args):

    seed = args.seed
    name = args.name
    folder = args.folder

    if name != '':
        name = name + '_'

    
    os.chdir(folder)
    os.chdir(os.pardir)

    train_set = os.getcwd() + "/" + name + "train"
    os.makedirs(name + "train", exist_ok=True)
    test_set = os.getcwd() + "/" + name + "test"
    os.makedirs(name + "test", exist_ok=True)
    validation_set = os.getcwd() + "/" + name + "validation"
    os.makedirs(name + "validation", exist_ok=True)

    documents = []
    for item in os.listdir(folder):
        if not item.startswith('.') and os.path.isfile(os.path.join(folder, item)):
            documents.append(folder + "/" + item)
    
    train , test = train_test_split(documents, test_size = 0.2, random_state = seed)
    
    test, val = train_test_split(test, test_size = 0.5, random_state = seed)

    #copy files to the train, test, and validation set folders
    for file in range(0,len(train)):
        shutil.copy(train[file],train_set)
    
    for file in range(0,len(val)):
        shutil.copy(val[file],validation_set)
    
    for file in range(0,len(test)):
        shutil.copy(test[file],test_set)

    print("All documents: ", len(documents))
    print("Documents in train set: ", len(train))
    print("Documents in validation set: ", len(val))
    print("Documents in test set: ", len(test))


   
    

if __name__ == '__main__':
    args = get_args()
    main(args)