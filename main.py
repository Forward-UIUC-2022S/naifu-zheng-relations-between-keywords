import time
import FindRelationship, Search
import SnippetDetails
import re
import nltk.data
import nltk 
from nltk import word_tokenize
import json
import bz2
import pickle
import _pickle as cPickle

target_json = open("filtered_arxiv.json")
input_arxiv = json.load(target_json)

FindRelationship.FindRelationship("neural network", "deep learning", input_arxiv, 3, True)


# Test the output and the runtime of FindRelationshipJson
start = time.time()
FindRelationship.FindRelationshipJson("machine learning", "linear regression", input_arxiv)
FindRelationship.FindRelationshipJson("augmented reality", "computer vision", input_arxiv)
FindRelationship.FindRelationshipJson("Btree", "Data Structure", "filtered_arxiv.json")
FindRelationship.FindRelationshipJson("data mining", "feature selection", input_arxiv)
FindRelationship.FindRelationshipJson("machine learning", "linear regression", input_arxiv)
#FindRelationship.FindRelationshipJson("query processing", "query plan", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("software engineering", "operating system", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("data mining", "feature selection", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("social network", "recommender system", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("dynamic programming", "parallel computing", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("dynamic programming", "graph", "filtered_arxiv.json")
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("cloud computing", "web service", input_arxiv)
end = time.time()
print(end-start)

start = time.time()
FindRelationship.FindRelationshipJson("neural network", "deep learning", input_arxiv)
end = time.time()
print(end-start)


FindRelationship.LemmatizeEntireFile("/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv_lemmatized.json")
FindRelationship.FindRelationshipJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json")
FindRelationship.FindRelationshipModifiedJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv_lemmatized.json")
print(FindRelationship.SearchGoogle("Btree", "Data Structure"))
FindRelationship.FindRelationshipModifiedJson("Tree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv_lemmatized.json")


# Test the functionality of SearchGoogleList()
print(Search.SearchGoogleList("natural language processing", ["lexical analysis","recommend system"]),"\n")
print(Search.SearchGoogleList("machine learning", ["linear regression","recommend system"]),"\n")



# Test the functionality of deepSearch
start = time.time()
print(Search.deepSearch("https://towardsdatascience.com/introduction-to-machine-learning-algorithms-linear-regression-14c4e325882a", "Linear Regression is an algorithm that every Machine Learning enthusiast must know and it is also the right place to start for people who"))
print(Search.deepSearch("https://stackoverflow.com/questions/16690249/what-is-the-difference-between-dynamic-programming-and-greedy-approach", "Greedy algorithm have a local choice of the sub-problems whereas Dynamic programming would solve the all sub-problems and then select one that would lead to an"))
print(Search.deepSearch("https://www.oak-tree.tech/blog/data-science-nlp", "Lexical analysis is the process of trying to understand what words mean, intuit their context, and note the relationship of one word to others. It is often the"))
end = time.time()
print(end-start)

#Test the functionality of SearchGoogle
start = time.time()
print(Search.SearchGoogle("machine learning", "linear regression"))
print(Search.SearchGoogle("machine learning", "recommend system",True))
print(Search.SearchGoogle("cloud computing", "distributed system",False))
print(Search.SearchGoogle("virtual reality", "computer vision",False))
print(Search.SearchGoogle("data mining", "feature selection",True))
end = time.time()
print(end-start)
