import spacy
from SnippetDetails import SnippetDetails
#import nltk import Tree
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
from urllib.request import Request, urlopen
import requests

from bs4 import BeautifulSoup

from googlesearch import search

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
        processed = nlp(snippet)
        print("\nstart of snippet:\n")
        print(snippet)
        for token in processed:
                # searching for dependencies between the keywords
                # don't care about case sensitivity
                if (token.text.casefold() == word_one.casefold()):
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

                if (token.text.casefold() == word_two.casefold()):
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
        google_result = SearchGoogle(word_one, word_two)
        snippet_list.extend(google_result)
        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet.score)

        print(scores)

def FindRelationshipJson(word_one, word_two, json_path, n=3):
        snippet_list = SearchJsonFile(word_one, word_two, json_path)
        google_result = SearchGoogle(word_one, word_two)
        snippet_list.extend(google_result)
        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet.score)

        print(scores)

def Lemmatization(words):
        processed = nlp(words)
        result = ""
        for token in processed:
                result += token.lemma_
        return result

def SearchJsonFile(word_one, word_two, path):
        snippets = []
        with open(path) as json_file:
                json_data = json.load(json_file)
                # simplify words down into lemmmas, so that the words can be found
                simplified_one = Lemmatization(word_one)
                simplified_two = Lemmatization(word_two)
                # search for abstracts that fit the expected path
                for value in json_data:
                        #simplified_abstract = Lemmatization(value['abstract'])
                        compare = value['abstract'].replace(" ", "")
                        # check each sentence
                        sentences = compare.split(".")
                        for i in range(len(sentences)):
                                if (simplified_one in sentences[i]) or (simplified_two in sentences[i]):
                                        snippets.append(value['abstract'].split(".")[i] + ".")
                        

        return snippets

def SearchGoogle(word_one, word_two):
        snippets = []
        # replace space with + for google query
        item_one = word_one.replace(' ', '+')
        item_two = word_two.replace(' ', '+')
        google_query = 'https://www.google.com/search?q='+item_one+'+'+item_two
        request_results = Request(google_query, headers={'User-Agent': 'Mozilla/5.0'})
        search_results = urlopen(request_results).read()
        #print(search_results)

        # parse the html file returned by google
        #r = requests.get(google_query)
        #search_results = r.text
        #soup = BeautifulSoup(search_results, 'html.parser')
        #print(soup.beautify())
        #for s in soup.find_all(id="rhs_block"):
        #        print(s.text)
        #for i in soup.find_all('div',{'class':'post-info-wrap'}):
        #        link = i.find('a',href=True)
        #        if link != None:
        #                print(link['href'])
        #urls = []
        #for searchWrapper in soup.find_all('h3', {'class':'r'}):
        #        urls.append(searchWrapper.find('a')["href"]) 
        #print(soup.prettify())

        #google_results = search(google_query, tld="co.in", num=10, stop=10, pause=2)
        #for link in google_results:
        #        print(link)
        #with requests.Session() as s:
        #        headers = {
        #                "referer":"referer: https://www.google.com/",
        #                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        #                }
        #        s.post(google_query, headers=headers)
        #        response = s.get(google_query, headers=headers)
        #        soup = BeautifulSoup(response.text, 'html.parser')
        #        links = soup.findAll("a")
        #print(links)
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


