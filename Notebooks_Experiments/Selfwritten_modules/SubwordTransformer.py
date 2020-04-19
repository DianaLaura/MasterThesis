#implementation according to Sennrich2016, p. 4

import re
import collections
from collections import defaultdict
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class SubwordTransformer(BaseEstimator, TransformerMixin):
    subwords = collections.defaultdict(int)
    occurrences = [[]]
    feature_names = []

           
    def get_feature_names(self):
        return(self.feature_names)
    def get_vocab(self):
        return self.vocab

    def get_subwords(self):
        return self.subwords

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
        for key in self.vocab.items():
            new_key = key[0].replace(pattern,w_out)
            val = key[1]
            vocab_updated[new_key] = val          
                        
        self.vocab = vocab_updated
 
    def fit(self, X, y=None):
        for doc in X:
            text = self.tokenizer(doc)        
            for word in text:
                word = word.strip()
                charlist = list(word.lower())
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
            pair = str(best[0] + best[1])
            self.subwords[pair] += pairs[best]
            self.__update_vocab(best, pairs)
        self.feature_names = list(self.subwords.keys())
        return self

    def transform(self, X, y=None):
        occurrences = []
        for doc in X:
            new_row = []
            for pair in range(0, len(self.feature_names)):
                new_row.append(len(re.findall(self.feature_names[pair], doc)))
            occurrences.append(new_row)
        
        
        return np.asarray(occurrences)

