#
#Based on code from Dr. Paul Cook, UNB
#

import math, re
import sys
#Do not use the following libraries for your code
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# A simple tokenizer. Applies case folding
def tokenize(s):
    tokens = s.lower().split()
    trimmed_tokens = []
    for t in tokens:
        if re.search('\w', t):
            # t contains at least 1 alphanumeric character
            t = re.sub('^\W*', '', t) # trim leading non-alphanumeric chars
            t = re.sub('\W*$', '', t) # trim trailing non-alphanumeric chars
        trimmed_tokens.append(t)
    return trimmed_tokens

# A most-frequent class baseline
class Baseline:
    def __init__(self, klasses):
        self.train(klasses)

    def train(self, klasses):
        # Count classes to determine which is the most frequent
        klass_freqs = {}
        for k in klasses:
            klass_freqs[k] = klass_freqs.get(k, 0) + 1
        self.mfc = sorted(klass_freqs, reverse=True, 
                          key=lambda x : klass_freqs[x])[0]
    
    def classify(self, test_instance):
        return self.mfc

#A logistic regression baseline
class LogReg:
    def __init__(self, texts, klasses):
        
        self.train(texts, klasses)

    def train(self, train_texts, train_klasses):
        # sklearn provides functionality for tokenizing text and
        # extracting features from it. This uses the tokenize function
        # defined above for tokenization (as opposed to sklearn's
        # default tokenization) so the results can be more easily
        # compared with those using NB.
        # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
        self.count_vectorizer = CountVectorizer(analyzer=tokenize)
        # train_counts will be a DxV matrix where D is the number of
        # training documents and V is the number of types in the
        # training documents. Each cell in the matrix indicates the
        # frequency (count) of a type in a document.
        self.train_counts = self.count_vectorizer.fit_transform(train_texts)
        # Train a logistic regression classifier on the training
        # data. A wide range of options are available. This does
        # something similar to what we saw in class, i.e., multinomial
        # logistic regression (multi_class='multinomial') using
        # stochastic average gradient descent (solver='sag') with L2
        # regularization (penalty='l2'). The maximum number of
        # iterations is set to 1000 (max_iter=1000) to allow the model
        # to converge. The random_state is set to 0 (an arbitrarily
        # chosen number) to help ensure results are consistent from
        # run to run.
        # http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
        self.lr = LogisticRegression(multi_class='multinomial',
                                solver='sag',
                                penalty='l2',
                                max_iter=1000,
                                random_state=0)
        self.clf = self.lr.fit(self.train_counts, train_klasses)

    def classify(self, test_instance):
        # Transform the test documents into a DxV matrix, similar to
        # that for the training documents, where D is the number of
        # test documents, and V is the number of types in the training
        # documents.
        #test_counts = self.count_vectorizer.transform(test_texts)
        test_count = self.count_vectorizer.transform([test_instance])
        # Predict the class for each test document  
        #results = self.clf.predict(test_counts)
        return self.clf.predict(test_count)[0]

##Implement the lexicon-based baseline
#You may change the parameters to each function
'''class lexicon():
    def __init__(self):
        
    def train(self, train_texts, train_klasses):

    def classify(self, test_instance):
'''

##Implement the multinomial Naive Bayes model with smoothing
'''class NaiveBayes():
    def __init__(self):
        
    def train(self, train_texts, train_klasses):

    def classify(self, test_instance):
'''

##Implement the binarized multinomial Naive Bayes model with smoothing
'''class BinaryNaiveBayes():
    def __init__(self):
        
    def train(self, train_texts, train_klasses):

    def classify(self, test_instance):
'''


if __name__ == '__main__':
    
    sys.stdout.reconfigure(encoding='utf-8')

    # Method will be one of 'baseline', 'lr', 'lexicon', 'nb', or
    # 'nbbin'
    method = sys.argv[1]

    train_texts_fname = sys.argv[2]
    train_klasses_fname = sys.argv[3]
    test_texts_fname = sys.argv[4]
    
    train_texts = [x.strip() for x in open(train_texts_fname,
                                           encoding='utf8')]
    train_klasses = [x.strip() for x in open(train_klasses_fname,
                                             encoding='utf8')]
    test_texts = [x.strip() for x in open(test_texts_fname,
                                          encoding='utf8')]
    
    #Check which method is being asked to implement form user
    if method == 'baseline':
        classifier = Baseline(train_klasses)

    elif method == 'lr':
        # Use sklearn's implementation of logistic regression
        classifier = LogReg(train_texts, train_klasses)
    
    #Run the classify method for each instance
    results = [classifier.classify(x) for x in test_texts]

    #Create output file at given output file name
    #Store predictions in output file
    outFile = sys.argv[5]
    out = open(outFile, 'w', encoding='utf-8')
    for r in results:
        out.write(r + '\n')
    out.close()