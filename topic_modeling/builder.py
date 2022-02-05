
import pandas as pd
import re
import string
import scipy.sparse

from sklearn.feature_extraction.text import CountVectorizer
from gensim import matutils, models
from nltk import word_tokenize, pos_tag


class TopicsBuilder:
    
    def __init__(self, data):
        data = self._combine_dict_values(data)   
        data_df = self._make_data_frame(data)
        data = self._clean_data(data_df)
        data = self._nouns_only_data(data_df)

        cv = CountVectorizer(stop_words='english')
        self._dtm = self._make_document_term_matrix(data, cv)

        self._tdm = self._dtm.transpose()
        self._corpus = self._make_corpus()
        self._id2word = self._make_id2word_dict(cv)

        
    def _combine_dict_values(self, data):
        return {key: [self._combine_text(value)] for (key, value) in data.items()}

    def _combine_text(self, list_of_text):
        '''Takes a list of text and combines them into one large chunk of text.'''
        combined_text = ' '.join(list_of_text)
        return combined_text

    def _make_data_frame(self, data):
        pd.set_option('max_colwidth',150)
        data_df = pd.DataFrame.from_dict(data).transpose()
        data_df.columns = ['transcript']
        data_df = data_df.sort_index()
        return data_df

    def _clean_data(self, data_df):
        return pd.DataFrame(data_df.transcript.apply(self._clean_text))

    def _nouns_only_data(self, data_df):
        return pd.DataFrame(data_df.transcript.apply(self._nouns_text))

    def _nouns_text(self, text):
        '''Given a string of text, tokenize the text and pull out only the nouns.'''
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = word_tokenize(text)
        all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)] 
        return ' '.join(all_nouns)


    def _clean_text(self, text):
        '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
        text = text.lower()
        text = re.sub('\\[.*?\\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\\w*\\d\\w*', '', text)
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    def _make_document_term_matrix(self, data, cv):
        data_cv = cv.fit_transform(data.transcript)
        dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        dtm.index = data.index
        return dtm

    def _make_corpus(self):
        sparse_counts = scipy.sparse.csr_matrix(self._tdm)
        return matutils.Sparse2Corpus(sparse_counts)

    def _make_id2word_dict(self, cv):
        return dict((v, k) for k, v in cv.vocabulary_.items())

    def run_diagnose(self, num_of_topics, num_of_iter):
        self._lda = models.LdaModel(corpus=self._corpus,
                                    id2word=self._id2word,
                                    num_topics=num_of_topics,
                                    passes=num_of_iter)

    def get_probablities(self):
        return self._lda.print_topics()

    def get_topics(self):
        corpus = self._lda[self._corpus]
        topics = []

        for movie_topics in corpus:
            topic_index, _ = max(movie_topics,key=lambda t: t[1])
            topics.append(topic_index)

        return list(zip(self._dtm.index, topics))
