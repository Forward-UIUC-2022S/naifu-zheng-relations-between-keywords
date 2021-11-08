# Meaningful-Relations-Between-Keywords

## Overall Design
This module will receive an input of 2 keywords, and attempt to parse corpus:
https://arxiv.org/
along with google search results

and return up to three of the best sentences that describe the relationship between the two keywords

## Functions/Functional Design:
FindRelationship(String one, String two, int n=3):
The function will return a string list of max size n(default 3), which will include the the three snippets that best describe the relationship of the keywords based off web results and rankings.


FindRelationship(String one, String two, int n=3, String json_path):
In addition to web results, also search and rate strings from a json file.

FindRelationship(String one, String two, int n=3, String[] list):
Instead of searching the web or a file, the sentences are already given and can be searched for the best n snippets.

ScoreSentence(snippet, word_one, word_two):
Scores a snippet based off of the algorithm mentioned below, returning an integer value that can be negative, 0, or positive.

SearchJsonFile(word_one, word_two, path):
Searches through the inputted json file for sentences/snippets that contain word one and word two.




### Example:
When calling the function with keywords like
b-tree and data structures,

Up to three(default) example sentences that relate to these keywords can be returned, like
"A B-tree is a tree data structure that keeps data sorted and allows searches, insertions, and deletions in logarithmic amortized time"


### Algorithmic Design / Model Implementation:
Current Model:
After breaking down a snippet using SpaCy, 
apply predermined rules of syntax and sentence structure
in order to determine a score of the snippet
Return the highest snippet scores

Possible considerations in the future:
With rated sentences from predetermined rules,
a model can be created being trained from these sentences, 
and continue rating other sentences for possibly higher accuracy

Currently considered rules:
including both keywords
connected by dependency path, a higher score the closer the path
length of snippet
number of sentences
original rating(from google or json files)

Here is an overall flowchart that describes the process from input to output
![Overall Flowchart](https://github.com/Forward-UIUC-2021F/Meaningful-Relations-Between-Keywords/blob/main/Overall_Flowchart.png)

Here is a flowchart explaining how the snippets are scored
![Scoring Flowchart](https://github.com/Forward-UIUC-2021F/Meaningful-Relations-Between-Keywords/blob/main/Scoring.png)


### Packages:
natural language processing:
Spacy
Download using:
pip install -U spacy


Searching corpus arxiv using snapshot JSON file:
filtered_arxiv.json

Google web crawler:


