# Meaningful-Relations-Between-Keywords

## Overall Design
This module will receive an input of 2 keywords, and attempt to parse corpus(searching "abstract" element, but can be easily changed):
https://arxiv.org/
along with google search results

and return up to three of the best snippets that describe the relationship between the two keywords

## Functions/Functional Design:
FindRelationship(String word_one, String word_two, int n=3, bool deeper_web_search=False):
The function will return a string list of max size n(default 3), which will include the the three snippets that best describe the relationship of the keywords based off web results and rankings. Paramater deeper_web_search will attempt to search additional websites for better snippets if set as true.

FindRelationshipJson(String word_one, String word_two, json_path, int n=3, bool deeper_web_search=False):
Additional parameter to search a json file for additional snippets if needed.

FindRelationshipGivenSentences(String word_one, String word_two, String[] list, int n=3):
Instead of searching the web or a file, the sentences are already given and can be directly scored for the best n snippets. Only rates the list, does not attempt to find additional snippets.

ScoreSentence(snippet, word_one, word_two, base_score=0):
Scores a snippet based off of the algorithm mentioned below, returning an integer value that can be negative, 0, or positive. Starts with a default value of 0, but additional weights can be added. Returns a SnippetDetails object, where the score can be extracted taking score element(i.e. returned_object.score)

SearchJsonFile(word_one, word_two, path):
Searches through the inputted json file for sentences/snippets that contain word one and/or word two.

LemmatizeEntireFile(input_path, output_path):
Takes the lemma of the entire input json file and writes it into the output_path. Useful for better search accuracy for keywords. Should be used in conjunction with FindRelationshipModifiedJson

FindRelationshipModifiedJson(word_one, word_two, json_path, modified_json_path, n=3, deeper_web_search=False):
Uses modified_json_path to search for keywords, but still returns snippets from json_path. Note: json_path will need to be the same input_path given in LemmatizeEntireFile, otherwise the wrong snippet may be rated.


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


### Packages and Dependencies:
natural language processing:
Spacy
Download using:
pip install -U spacy

Copying files(only used for taking the lemma of entire files):
pip install shutil

Searching corpus arxiv using snapshot JSON file(one example file included):
filtered_arxiv.json

Google web requests:
using Requests python library:
pip install requests

Using TQDM to display progress bar:
https://github.com/tqdm/tqdm
Download using:
pip install tqdm

Urllib and unittest are part of the standard python library, no install needed.


### Example:
Once dependencies are installed, check to see everything works with the main file with 
LemmatizeEntireFile(input_path, output_path)
and
FindRelationshipJson(keyword_1,keyword_2,json_file)

When calling the function with keywords like
b-tree and data structures,

Up to three(default) example sentences that relate to these keywords can be returned, like
"A B-tree is a tree data structure that keeps data sorted and allows searches, insertions, and deletions in logarithmic amortized time"

### File Structure:
Meaningful-Relations-Between-Keywords/
    - README.md
    - FindRelationship.py/
    - Overall_Flowchart.png/
    - Scoring.png/
    - SnippetDetails.py/
    - __init__.py/
    - main.py/

Important files:
FindRelationship.py: holds all relevant functions
SnippetDetails.py: Class to hold each snippet results and details
main.py: main function for testing or running any needed 

### Issues and Future Work
* Deeper search option still needs to be implemented, currently the parameter does nothing
* Inconsistency of finding and rating snippets with keywords longer than 1 word (i.e. "data structure")
* Slow to find and store the lemma of all snippets in a given database
* Need to implement additional flexibility to searching the json file(needs manual input currently, default "abstract")
* Improve snippets taken from the web, lots of uneeded details at the end like date, site name, categories, etc.

### Demo Video
youtube link:
https://www.youtube.com/watch?v=BkGTvdV1ZM4&t=1s
[<img src="https://img.youtube.com/vi/BkGTvdV1ZM4/maxresdefault.jpg" width="50%">](https://youtu.be/BkGTvdV1ZM4)
