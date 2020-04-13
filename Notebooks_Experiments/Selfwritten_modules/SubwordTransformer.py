#implementation according to Sennrich2016, p. 4 and https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html#sklearn.preprocessing.FunctionTransformer

import re
import collections
from collections import defaultdict
import numpy as np

class SubwordTransformer:

  
    def __init__(self, tokenizer=None, number_of_merges=10):
        self.vocab = defaultdict(int)
        self.tokenizer = tokenizer
        self.number_of_merges = number of merges
    

    def __get_stats(self):

        pairs = collections.defaultdict(int)

        for word, freq in self.vocab.items():

            symbols = word.split(',')
            
            for i in range (0, len(symbols) - 1):
                pairs[symbols[i], symbols[i+1]] += freq
        
        return pairs

    def __update_vocab(self, pair):

        vocab_updated = defaultdict(int)
        for word in pair:
            w_out = str(pair[0] + pair[1])
            pattern = str(pair[0] + r',' + pair[1])
            print(pattern)
            print(w_out)

            for key in self.vocab.items():
                
                new_key = key[0].replace(pattern,w_out)
                val = key[1]
                vocab_updated[new_key] = val
            
            self.vocab = vocab_updated
    
    def bpe(self, data):
        #extract vocabulary from the data and store it in a dictionary with frequency counts
        for row in (0,(len(data)-1)):

            raw_text = data[row]
            
            text = self.tokenizer(data[row])
            
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
            self.__update_vocab(best)
            
        
        
        return self.vocab

 
    def get_vocab(self):
        return self.vocab

    """
    def inverse_BPE(subwords):

        return data

    """