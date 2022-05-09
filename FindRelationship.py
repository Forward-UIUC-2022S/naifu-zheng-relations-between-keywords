from Search import SearchJsonFile, SearchGoogleList, SearchGoogle, nlp
from tokenize import Pointfloat
from matplotlib.pyplot import title
import spacy
from SnippetDetails import SnippetDetails
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
from urllib.request import Request, urlopen

from operator import attrgetter
#from googlesearch import search
#from googlesearch.googlesearch import GoogleSearch

# progress bar
from tqdm import tqdm
import os, os.path

import os, os.path

# copying file
from shutil import copyfile


config = {
   "moves": None,
   "update_with_oracle_cut_size": 100,
   "learn_tokens": False,
   "min_action_freq": 30,
   "model": DEFAULT_PARSER_MODEL,
}


# default weighting for google results
google_base_weight = 100
google_weight_scale = 5
max_search_count = 20

# element to search in the json file, change to whatever is needed
element_to_search = "abstract"

#nlp = spacy.load("en_core_web_sm")

# add default dependency parsing with spacy
#nlp.add_pipe("parser", config=config)
# good sentence
google_one = "In computer science, a Btree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The Btree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "Btree is a data structure that store data in its node in sorted order"

def ScoreSentence(snippet, word_one, word_two, base_score = 0):
        snippet_details = SnippetDetails(snippet)
        snippet_details.score = base_score
        processed = nlp(snippet)
        #print("\nstart of snippet:\n")
        #print(Lemmatization("Machine Learning"))
        #print("********",processed)
        for token in processed:
                # searching for dependencies between the keywords
                # don't care about case sensitivity
                #print(str(token.text))
                if (token.text.lower() in word_one.lower()):
                        children = [child for child in token.children]
                        for child in children:
                                if (word_two in child.text):
                                        snippet_details.score += 200
                                        # if found, add score and stop searching
                                        break
                                grandchildren = [child for child in child.children]
                                for grandchild in grandchildren:
                                        if (word_one in grandchild.text):
                                                snippet_details.score += 100
                                                break

                if (token.text.lower() in word_two.lower()):
                        children = [child for child in token.children]
                        for child in children:
                                if (word_one in child.text):
                                        snippet_details.score += 200
                                        # if found, add score and stop searching
                                        break
                                grandchildren = [child for child in child.children]
                                for grandchild in grandchildren:
                                        if (word_one in grandchild.text):
                                                snippet_details.score += 100
                                                break

                # take one point off for each word in the snippet
                snippet_details.score -= 1


        if (word_one.lower() in snippet.lower()):
                snippet_details.score += 100
        if (word_two.lower() in snippet.lower()):
                snippet_details.score += 100

        return snippet_details

def FindRelationship(word_one, word_two, json_path,n, deeper_web_search):
        # TODO: search google and corpus for snippets of sentences containing
        # the relationship of word 1 and 2

        snippet_list = SearchJsonFile(word_one, word_two, json_path)

        scores = []
        cur_size = len(snippet_list)
        base_score = google_base_weight
        for i in range(cur_size):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score/2)
                scores.append(updated_snippet)

        google_result = SearchGoogle(word_one, word_two, deeper_web_search)
        snippet_list.extend(google_result)
        
        for i in range(cur_size, len(snippet_list)):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score)
                scores.append(updated_snippet)
                
                base_score -= google_weight_scale
                if (base_score < 0):
                        base_score = 0
        PrintBestScores(scores, n)
        return (word_one, word_two,snippet_list[:3])


def FindRelationshipJson(word_one, word_two, json_path, n=3, deeper_web_search=False):
        #with open(json_path) as json_file:
        snippet_list = SearchJsonFile(word_one, word_two, json_path)

        scores = []
        cur_size = len(snippet_list)
        base_score = google_base_weight
        for i in range(cur_size):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score/2)
                scores.append(updated_snippet)

        PrintBestScores(scores, n)

        return (word_one, word_two,snippet_list[:3])
       

# add additional argument for filtered json file,
def FindRelationshipModifiedJson(word_one, word_two, json_path, modified_json_path, n=3, deeper_web_search=False):
        snippet_list = SearchJsonFile(word_one, word_two, json_path, modified_json_path)

        scores = []
        cur_size = len(snippet_list)
        base_score = google_base_weight
        for i in range(cur_size):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score/2)
                scores.append(updated_snippet)

        google_result = SearchGoogle(word_one, word_two, deeper_web_search)
        snippet_list.extend(google_result)
        for i in range(cur_size, len(snippet_list)):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score)
                scores.append(updated_snippet)
                
                base_score -= google_weight_scale
                if (base_score < 0):
                        base_score = 0
        
        PrintBestScores(scores, n)

def FindRelationshipGivenSentences(word_one, word_two, list, n=3):
        scores = []
        for snippet in list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)
        PrintBestScores(scores, n)
        
def PrintBestScores(scores, n):
        #scores = scores.sort()
        scores.sort(key=attrgetter('score'))

        # for i in range(len(scores)):
        #         print(scores[i].score)

        if (n > len(scores)):
                print("Not enough good snippets found. Returning top " + str(len(scores)) + " snippets instead")

        snippet_count = min(len(scores), n)
        print("Printing top " + str(snippet_count) + " snippets")
        for i in range(snippet_count):
                cur_index = len(scores) - i - 1
                print("Snippet " + str(i) + " sentence:")
                print(scores[cur_index].string)
                print("With a score of " + str(scores[cur_index].score))






