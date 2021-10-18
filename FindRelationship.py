import spacy
from SnippetDetails import SnippetDetails
#import nltk import Tree
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
config = {
   "moves": None,
   "update_with_oracle_cut_size": 100,
   "learn_tokens": False,
   "min_action_freq": 30,
   "model": DEFAULT_PARSER_MODEL,
}

import json

nlp = spacy.load("en_core_web_sm")
# add default dependency parsing with spacy
#nlp.add_pipe("parser", config=config)
# good sentence
google_one = "In computer science, a B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The B-tree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "B-tree is a data structure that store data in its node in sorted order"

def ScoreSentence(snippet, word_one, word_two):
        snippet_details = SnippetDetails(snippet)
        print(type(snippet))
        processed = nlp(snippet)
        for token in processed:
                # searching for dependencies between the keywords
                # don't care about case sensitivity
                if (token.text.casefold() == word_one.casefold()):
                        if (word_two in token.children):
                                snippet_details.score += 200
                                # if found, add score and stop searching
                                break

                if (token.text.casefold() == word_two.casefold()):
                        if (word_one in token.children):
                                snippet_details.score += 200
                                # if found, add score and stop searching
                                break

                # take one point off for each word in the snippet
                snippet_details.score -= 1


        if (word_one in snippet):
                snippet_details.score += 100
        if (word_two in snippet):
                snippet_details.score += 100

        return snippet_details

def FindRelationship(word_one, word_two, n=3):
        # TODO: search google and corpus for snippets of sentences containing
        # the relationship of word 1 and 2

        # currently using hard coded phrases
        snippet_list = [google_one, google_two, google_three]
        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet.score)

        print(scores)

def FindRelationshipJson(word_one, word_two, json_path, n=3):
        snippet_list = searchJsonFile(word_one, word_two, json_path)
        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet.score)

        print(scores)

def searchJsonFile(word_one, word_two, path):
        snippets = []
        with open(path) as json_file:
                json_data = json.load(json_file)
                # search for abstracts that fit the expected path
                for value in json_data.values():
                        if (word_one in value['abstract']) and (word_two in value['abstract']):
                                snippets.append(value['abstract'])

        return snippets

def searchGoogle(word_one, word_two):
        snippets = []
        return snippets

## helper function taken from
## https://stackoverflow.com/questions/42824129/dependency-parsing-tree-in-spacy
#def to_nltk_tree(node):
#        if node.n_lefts + node.n_rights > 0:
#            return Tree(token_format(node),
#                       [to_nltk_tree(child) 
#                        for child in node.children]
#                   )
#        else:
#            return token_format(node)


