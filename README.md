# Meaningful-Relations-Between-Keywords

## Overall Design
This module will receive an input of 2 keywords, and attempt to parse corpus:
https://arxiv.org/
along with google search results

and return up to three of the best sentences that describe the relationship bewteen the two keywords

## Functions:
FindRelationship(String one, String two):

The function will return a string list of max size 3, which will include the the three sentences that best 


### Example:
When calling the function with keywords like
b-tree and data structures,

Up to three example sentences that relate to these keywords can be returned, like
"A B-tree is a tree data structure that keeps data sorted and allows searches, insertions, and deletions in logarithmic amortized time"


### Model Implementation:

Work in progress:
rate based on syntax of summary sentences when training a model
Unsure of what kind of model to use
Which factors are important in good sentences,

