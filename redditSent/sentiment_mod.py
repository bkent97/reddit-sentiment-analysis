import nltk
from nltk.tokenize import word_tokenize
import random
import codecs
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import pickle

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers

	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)

	def confidence(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		
		choice_votes = votes.count(mode(votes))
		conf = choice_votes / len(votes)
		return conf

documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()


word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

def find_features(document):
	words = word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)

	return features

featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
#print(len(featuresets))

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

open_file = open("pickled_algos/orig_classifier.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

#MultinomialNB
open_file = open("pickled_algos/mnb_classifier.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

#BernoulliNB
open_file = open("pickled_algos/bern_classifier.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

#Logistic Regression
open_file = open("pickled_algos/log_classifier.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

#SGD
open_file = open("pickled_algos/sgd_classifier.pickle", "rb")
SGDClassifier_classifier = pickle.load(open_file)
open_file.close()

#LinearSVC
open_file = open("pickled_algos/lin_classifier.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

#NuSVC
open_file = open("pickled_algos/nu_classifier.pickle", "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()

#takes all algorithms into account
voted_classifier = VoteClassifier(classifier, 
				MNB_classifier, 
				BernoulliNB_classifier, 
				LogisticRegression_classifier, 
				SGDClassifier_classifier, 
				LinearSVC_classifier, 
				NuSVC_classifier)
print("Voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)

def sentiment(text):
	feats = find_features(text)
	return voted_classifier.classify(feats), voted_classifier.confidence(feats)

