#implementation according to Sennrich2016, p. 4 and https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html#sklearn.preprocessing.FunctionTransformer

import re
import collections
from collections import defaultdict

class SubwordTransformer:

  
    def __init__(self, tokenizer=None):
        self.vocab = defaultdict(int)
        self.tokenizer = tokenizer
    

    def __get_stats(self):

        pairs = collections.defaultdict(int)

        for word, freq in self.vocab.items():
            symbol = list(word)
            for i in range (0, len(symbol) - 1):
                pairs[symbol[i], symbol[i+1]] += freq
        
        return pairs

    def __merge_vocab(self, pair):
    
        bigram = re.escape(' '.join(pair))
        print(bigram)
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in pair:
            w_out = p.sub(''.join(pair), word)
            print(w_out)
            self.vocab[w_out] +=1
        return self.vocab
    
    def bpe(self, data):
        #extract vocabulary from the data and store it in a dictionary with frequency counts
        for row in (0,(len(data)-1)):

            raw_text = data[row]
            
            text = self.tokenizer(data[row])
            
            for word in text:
                self.vocab[word] += 1
            

        num_merges = 1

        for i in range(0, num_merges):
            pairs = self.__get_stats()
            best = max(pairs, key=pairs.get)
            self.vocab = self.__merge_vocab(best)
            
            
            
        return self.vocab

 
    def get_vocab(self):
        return self.vocab

    """
    def inverse_BPE(subwords):

        return data

    """