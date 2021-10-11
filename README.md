# Meaningful-Relations-Between-Keywords

## Overall Design
This module will receive an input of 2 keywords, and attempt to parse corpus:
https://arxiv.org/
along with google search results

and return up to three of the best sentences that describe the relationship between the two keywords

## Functions:
FindRelationship(String one, String two):

The function will return a string list of max size 3, which will include the the three sentences that best describe the relationship of the keywords based off web results and rankings.


### Example:
When calling the function with keywords like
b-tree and data structures,

Up to three example sentences that relate to these keywords can be returned, like
"A B-tree is a tree data structure that keeps data sorted and allows searches, insertions, and deletions in logarithmic amortized time"


### Model Implementation:
Work in progress:
rate based on syntax of summary sentences when training a model
Unsure of what kind of model to use
Which factors are important in good sentences.
supervised, unsupervised

Current Model:
After breaking down a snippet using SpaCy, 
apply predermined rules of syntax and sentence structure
in order to determine a score of the snippet
Return the highest snippet scores

Currently considered rules:
including both keywords
connected by dependency path


### Packages:
natural language processing:
Spacy
Download using:
pip install -U spacy


Searching corpus () API:
https://arxiv.org/help/api/basics

Google web crawler:

