---
title: Twitter analysis
author: Evan
categories:
  - Data
tags:
  - python
  - data analysis
---

Statistical methods for modeling and analyzing data are all
the buzz, and have been for a while now. Tooling has come a long way, as have educational
resources and open source projects. I'll present here my application of the walkthrough
posted by Marco Bonzanini on his [Blog](https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/).
It was a good start to learn the fundamentals of semantic analysis, and a soft introduction
to programming with python.

*Harvesting Tweets*

My data harvesting efforts started with the node.js twitter package on npm. Harvesting
data from twitter's streaming api is conveniently supported by many packages produced
by the community. Unfortunately, its had to tell which package is the best fit. The
node twitter package required a custom modification to handle stream interruptions, which,
though fairly trivial, caused the service to stop unexpectedly when the connection was dropped.

I found the [twarc](https://github.com/DocNow/twarc) library to be a handy and painless way to quickly configure a new twitter application,
and there are associate utilities that made for easy bounds checking. Because I want to run
multiple configurations at once, I did end up writing configuration code in a twitter service application
that is responsible for establishing multiple twitter streams and filtering the results beyond what the
streaming api filters enable.

With a collection of tweets, it was fairly easy to iterate over them and apply our analysis.

*Classifier*

The classifier implemented is termed PMI-IR proposed by Turney(2002) [http://www.aclweb.org/anthology/P02-1053.pdf](http://www.aclweb.org/anthology/P02-1053.pdf). It is a straitforward unsupervised learning technique
that evaluates the polarity and its valence based on closeness of terms to those from an apriori positive and negative lexicon,
where closeness is defined by the number of times the words cooccur in the data). These lexicon were obtained from
[Bing Liu](http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon) at the authors recommendation.

With a corpus of tweets, the a processing pass iterates over each tweet to count the frequency of each term and to
build a cooccurrence matrix to track how often terms are used in the same text.

```python
def process_tweets(self, tweet):
    """Process tweet data and store in private variables
    Args:
        tweet (obj): tweet payload
    """

    text = tweet['text']
    # Count terms only (no hashtags, no mentions)
    tokens = preprocess(text)
    terms_stop = terms_only(tokens)
    self._count_terms_stop.update(terms_stop)
    self.__cooccurrence.apply(terms_stop)

    self.tweets.append({
        'text': tweet['text'],
    })
```

From these counts, we can create a PMI matrix for all terms by using the document frequency of all terms to compute the
probability of encountering a term and to divide it by the probabilty of encountering a cooccurrring term,
then transforming the result by applying a log function.

```python
def pmi(self):
    """Calculate closeness to known lexicon with assigned polarity
    Returns:
        pmi The Pointwise Mutual Information
    """

    ## for each tweet, go through and calculate a SO
    n_docs = len(self.tweets)
    p_t = {}
    p_t_com = defaultdict(lambda : defaultdict(int))

    for term, n in self._count_terms_stop.items():
        p_t[term] = (n / n_docs) # probability of observing the term
        for t2 in self.com[term]:
            p_t_com[term][t2] = self.com[term][t2] / n_docs # probability of cooccurrence

    pmi = defaultdict(lambda : defaultdict(int))
    for t1 in p_t:
        for t2 in self.com[t1]:
            denom = p_t[t1] * p_t[t2]
            term1, term2 = sorted([t1, t2])
            pmi[term1][term2] = math.log((p_t_com[term1][term2]) / (denom), 2)
    return pmi
```

Once we have all PMI scores for all pairs of words, we can compute a term's orientation valence by aggregating
the PMI of a term and each term in the positive and negative lexicon.

```python
def orientation_valence(self, pmi):
    """calcluate the probability of a term and its cooccurrences to determine a
    valence score
    See: https://marcobonzanini.com/2015/05/17/mining-twitter-data-with-python-part-6-sentiment-analysis-basics/
    Returns:
        (dict) sentiment orientation valence for terms
    """
    semantic_orientation = {}
    for term, n in self._count_terms_stop.items():
        try:
            positive_assoc = sum(self.get_pmi(pmi, term, tx) if tx != term else 1.5 for tx in positive_vocab)
            negative_assoc = sum(self.get_pmi(pmi, term, tx) if tx != term else 1.5 for tx in negative_vocab)
            semantic_orientation[term] = positive_assoc - negative_assoc

        except:
            pass

    semantic_sorted = sorted(semantic_orientation.items(),
                        key=operator.itemgetter(1),
                        reverse=True)
    return semantic_orientation
```

We then have an orientation for each
term, and the semantic orientation of a sentence can be the aggregate orientation of its consituent words.

*Implementation*

I followed the tutorial with two exceptions. The first was to sort the pmi indices because of the way the
cooccurrence matrix was created requires that these terms be in order. The second is to add a bias to the terms
from our lexicon to increase the chance of them having a positive or negative polarity, to offset deviations
due to a PMI that has changed its meaning due to the context it is frequently found in.

A set of tweets

    tweets = [{ u'text': u'What a useless widget' },
            { u'text': u'I was angry before but now I am over it' },
            { u'text': u'I could cry but I would rather be happy' },
            { u'text': u'Cry because you are terrible' },
            { u'text': u'Where have all the sunny days gone?' }]

and a vocabulary of words with known polarity


    positive_vocab = [
        'good', 'nice', 'great', 'awesome', 'outstanding', 'sunny',
        'fantastic', 'terrific', ':)', ':-)', 'like', 'love', 'happy'
        # shall we also include game-specific terms?
        # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
    ]
    negative_vocab = [
        'angry', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
        'sad', 'cry'
        # 'defeat', etc.
    ]

produces a semantic orientation for each of the terms

    {u'gone': 2.321928094887362,
    u'widget': -2.321928094887362,
    u'would': 1.0,
    u'rather': 1.0,
    u'could': 1.0,
    u'cry': -1.5,
    u'sunny': 1.5,
    u'terrible': -2.821928094887362,
    u'days': 2.321928094887362,
    u'useless': -1.5,
    u'angry': -1.5,
    u'happy': 0.17807190511263782}


and yeilds an aggregate orentation for each sentence

    [
      {u'text': u'Where have all the sunny days gone?', 'score': 0.7679820237218405},
      {u'text': u'I could cry but I would rather be happy', 'score': 0.1864524339014042},
      {u'text': u'I was angry before but now I am over it', 'score': -0.15},
      {u'text': u'Cry because you are terrible', 'score': -0.8643856189774723},
      {u'text': u'What a useless widget', 'score': -0.9554820237218405}
    ]



The python code is below

    from __future__ import division
    from nltk.corpus import stopwords
    import string
    import re
    import nltk
    from collections import defaultdict
    from collections import Counter
    import math
    import operator

    nltk.download('punkt')
    nltk.download('stopwords')

    positive_vocab = [
        'good', 'nice', 'great', 'awesome', 'outstanding', 'sunny',
        'fantastic', 'terrific', ':)', ':-)', 'like', 'love', 'happy'
        # shall we also include game-specific terms?
        # 'triumph', 'triumphal', 'triumphant', 'victory', etc.
    ]
    negative_vocab = [
        'angry', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
        'sad', 'cry'
        # 'defeat', etc.
    ]

    regex_str = [
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]

    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE)

    def tokenize(s):
        """Convert a string of words into an array of word tokens"""
        return tokens_re.findall(s)

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

    def preprocess(s):
        tokens = tokenize(s)
        return [token.lower() for token in tokens]

    def terms_only(terms):
        """Count terms only (no hashtags, no mentions)"""
        return [term for term in terms
                    if term not in stop and
                    not term.startswith(('#', '@'))]


    class Cooccurrence:
        """Apply term tokens to a coocurrences dictionary to count the terms"""
        def __init__(self):
            self.__com = defaultdict(lambda : defaultdict(int))

        @property
        def com(self):
            return self.__com

        def apply(self, terms_only):
            for i in range(len(terms_only)-1):
                for j in range(i+1, len(terms_only)):
                    w1, w2 = sorted([terms_only[i], terms_only[j]])

                    if w1 != w2:
                        self.__com[w1][w2] += 1


    class Classifier:
        """Track tweet statistics by applying counts to terms
        Apply statistics like frequency counts, bigrams, etc
        """

        def __init__(self):
            self.__cooccurrence = Cooccurrence()
            self._count_terms_stop = Counter()
            self.tweets = []

        @property
        def com(self):
            return self.__cooccurrence.com

        def process_tweets(self, tweet):
            """Process tweet data and store in private variables
            Args:
                tweet (obj): tweet payload
            """

            text = tweet['text']
            # Count terms only (no hashtags, no mentions)
            tokens = preprocess(text)
            terms_stop = terms_only(tokens)
            self._count_terms_stop.update(terms_stop)
            self.__cooccurrence.apply(terms_stop)

            self.tweets.append({
                'text': tweet['text'],
            })

        def apply_orientation(self, tweets, so):
            """Apply semantic orientation to tweet

            Args:
                texts (str[]): array of all tweets
                so (dict): orientation rules
            """
            for t in tweets:
                tokens = preprocess(t['text'])
                value = 0
                for term in terms_only(tokens):
                    value += so[term]
                t['score'] = value / len(tokens)

            tweets_sorted = sorted(tweets, key=lambda x: x['score'], reverse=True)
            return tweets_sorted

        def pmi(self):
            """Calculate closeness to known lexicon with assigned polarity
            Returns:
                pmi The Pointwise Mutual Information
            """

            ## for each tweet, go through and calculate a SO
            n_docs = len(self.tweets)
            p_t = {}
            p_t_com = defaultdict(lambda : defaultdict(int))

            for term, n in self._count_terms_stop.items():
                try:
                    p_t[term] = (n / n_docs) # probability of observing the term
                    for t2 in self.com[term]:
                        p_t_com[term][t2] = self.com[term][t2] / n_docs # probability of cooccurrence
                except:
                    pass

            pmi = defaultdict(lambda : defaultdict(int))
            for t1 in p_t:
                for t2 in self.com[t1]:
                    try:
                        denom = p_t[t1] * p_t[t2]
                        term1, term2 = sorted([t1, t2])
                        #print "%s and %s for %s-%s" % (p_t_com[t1][t2], denom, t1, t2)
                        pmi[term1][term2] = math.log((p_t_com[term1][term2]) / (denom), 2)
                    except:
                        pass
            return pmi

        def get_pmi(self, lookup, t1, t2):
            """Order our terms because of our triangle matrix
            Args:
                lookup (dict): our pmi dictionary
                t1 (str): the first term
                t2 (str): the second term
            """
            term1, term2 = sorted([t1,t2])
            return lookup[term1][term2]

        def orientation_valence(self, pmi):
            """calcluate the probability of a term and its cooccurrences to determine a
            valence score
            See: https://marcobonzanini.com/2015/05/17/mining-twitter-data-with-python-part-6-sentiment-analysis-basics/
            Returns:
                (dict) sentiment orientation valence for terms
            """
            semantic_orientation = {}
            for term, n in self._count_terms_stop.items():
                try:
                    positive_assoc = sum(self.get_pmi(pmi, term, tx) if tx != term else 1.5 for tx in positive_vocab)
                    negative_assoc = sum(self.get_pmi(pmi, term, tx) if tx != term else 1.5 for tx in negative_vocab)
                    semantic_orientation[term] = positive_assoc - negative_assoc

                except:
                    pass

            semantic_sorted = sorted(semantic_orientation.items(),
                                key=operator.itemgetter(1),
                                reverse=True)
            return semantic_orientation

    if __name__ == '__main__':
        tweets = [{ u'text': u'What a useless widget' },
            { u'text': u'I was angry before but now I am over it' },
            { u'text': u'I could cry but I would rather be happy' },
            { u'text': u'Cry because you are terrible' },
            { u'text': u'Where have all the sunny days gone?' }]

        classifier = Classifier()

        for tweet in tweets:
            classifier.process_tweets(tweet)

        pmi = classifier.pmi()
        valence = classifier.orientation_valence(pmi)
        so = classifier.apply_orientation(tweets, valence)
        print(so[-10:])