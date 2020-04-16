#implementation according to Sennrich2016, p. 4

import re
import collections
from collections import defaultdict
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class SubwordTransformer(BaseEstimator, TransformerMixin):
    subwords = collections.defaultdict(int)
    occurrences = [[]]
    current_features = collections.defaultdict(int)
    feature_names = []

  
    def __init__(self, tokenizer=None, number_of_merges=10):
        self.vocab = defaultdict(int)
        self.tokenizer = tokenizer
        self.number_of_merges = number_of_merges
    

    def __get_stats(self):

        pairs = defaultdict(int)
        
        for word, freq in self.vocab.items():

            symbols = word.split(',')
            
            for i in range (0, len(symbols) - 1):
                pairs[symbols[i], symbols[i+1]] += freq
        
        return pairs

    def __update_vocab(self, pair, pairs):

        vocab_updated = defaultdict(int)
        
            
        w_out = str(pair[0] + pair[1])
        pattern = str(pair[0] + r',' + pair[1])
        self.subwords[w_out] += pairs[pair]
           
        self.current_features[w_out] += pairs[pair]
            
        for key in self.vocab.items():
            new_key = key[0].replace(pattern,w_out)
            val = key[1]
            vocab_updated[new_key] = val          
                        
        self.vocab = vocab_updated

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for doc in X:
            self.vocab = collections.defaultdict(int)
            self.current_features = collections.defaultdict(int)
            subwords_old = self.subwords

            #extract vocabulary from the data and store it in a dictionary with frequency counts
            
            text = self.tokenizer(doc)        
            for word in text:
                word = word.strip()
                charlist = list(word)
                try:
                    final_word = charlist[1]
                    for item in  range(2, len(charlist)-1):
                        final_word = final_word + ',' + charlist[item]     

                except IndexError:
                    final_word = charlist[0]

                self.vocab[final_word] += 1
            
           
            for i in range(0, self.number_of_merges):
                pairs = self.__get_stats()
                best = max(pairs, key=pairs.get)
                self.__update_vocab(best, pairs)
            
            #load features and counts of current document into a nested list that can be transformed into an array
            new_row = []
            
            for word in self.occurrences[0]:
                if word in self.current_features:
                    new_row.append(self.current_features[word])
                else:
                    new_row.append(0)
            
            for word, val in self.current_features.items():
                if word not in subwords_old.items():
                    self.occurrences[0].append(word)
                    if len(self.occurrences) > 1:
                        for i in range(1, len(self.occurrences)):
                            self.occurrences[i].append(0)
                    new_row.append(val)
            
            self.occurrences.append(new_row)
        

        #encode feature names into integer
        
        
        self.feature_names = self.occurrences[0]
       
        
        return np.asarray(self.occurrences)

    
    def get_feature_names(self):
        return(self.feature_names)
    def get_vocab(self):
        return self.vocab

    def get_subwords(self):
        return self.subwords

    """
    def inverse_BPE(subwords):

        return data

    """