import spacy
from SnippetDetails import SnippetDetails
#import nltk import Tree
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
from urllib.request import Request, urlopen
import requests

from bs4 import BeautifulSoup
from operator import attrgetter
#from googlesearch import search
from googlesearch.googlesearch import GoogleSearch

# progress bar
from tqdm import tqdm

# copying file
from shutil import copyfile

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
google_one = "In computer science, a Btree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The Btree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "Btree is a data structure that store data in its node in sorted order"

def ScoreSentence(snippet, word_one, word_two):
        snippet_details = SnippetDetails(snippet)
        processed = nlp(snippet)
        #print("\nstart of snippet:\n")
        #print(Lemmatization("Machine Learning"))
        #print(snippet)
        for token in processed:
                # searching for dependencies between the keywords
                # don't care about case sensitivity
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
                scores.append(updated_snippet)

        PrintBestScores(scores, n)

def FindRelationshipJson(word_one, word_two, json_path, n=3):
        snippet_list = SearchJsonFile(word_one, word_two, json_path)
        google_result = SearchGoogle(word_one, word_two)
        snippet_list.extend(google_result)

        snippet_list.append(google_one)
        snippet_list.append(google_two)
        snippet_list.append(google_three)

        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)
        PrintBestScores(scores, n)
        
def FindRelationshipModifiedJson(word_one, word_two, json_path, modified_json_path, n=3):
        snippet_list = SearchJsonFile(word_one, word_two, json_path, modified_json_path)
        google_result = SearchGoogle(word_one, word_two)
        snippet_list.extend(google_result)

        snippet_list.append(google_one)
        snippet_list.append(google_two)
        snippet_list.append(google_three)

        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)
        PrintBestScores(scores, n)
        
def PrintBestScores(scores, n):
        #scores = scores.sort()
        scores.sort(key=attrgetter('score'))

        for i in range(len(scores)):
                print(scores[i].score)

        if (n > len(scores)):
                print("Not enough good snippets found. Returning top " + len(scores) + " snippets instead")

        snippet_count = min(len(scores), n)
        print("Printing top " + str(snippet_count) + " snippets")
        for i in range(snippet_count):
                cur_index = len(scores) - i - 1
                print("Snippet " + i + " sentence:")
                print(scores[cur_index].string)
                print("With a score of " + str(scores[cur_index].score))

def Lemmatization(words):
        processed = nlp(words)
        result = ""
        for token in processed:
                result += token.lemma_
        return result

def LemmatizeEntireFile(input_path, output_path):

        # create or delete output_path
        # try:
        #         open(output_path, "w")
        #         print("output path file found, overwriting contents")
        # except IOError:
        #         print("output path file not found, creating one instead")
        
        copyfile(input_path, output_path)

        with open(output_path, "r") as output_file:
                json_data = json.load(output_file)
                print("LENGTH =========== ")
                print(len(json_data))
                #cut_json = json_data[:295306]
                size_to_lemma = 50000
                json_data = json_data[:size_to_lemma]
                for i in tqdm(range(size_to_lemma)):
                        # value = json_data[i]
                        json_data[i]['abstract'] = Lemmatization(json_data[i]['abstract'])
                        # lemmatized = Lemmatization(value['abstract'])
                        # to_write = {
                        #         "abstract" : lemmatized,
                        # }
                        # json.dump(to_write, output_file)
                output_file.close()
        with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(json_data))

def SearchJsonFile(word_one, word_two, path, modified_json_path=None):
        snippets = []
        with open(path) as json_file:
                simplified_one = Lemmatization(word_one).lower()
                simplified_two = Lemmatization(word_two).lower()
                # lemmatized json file has been initialized already
                if modified_json_path != None:
                        with open(modified_json_path) as modified_json_file:
                                json_data = json.load(json_file)
                                modified_json_data = json.load(modified_json_file)
                                length = min(len(json_data), len(modified_json_data))
                                for i in range(length):
                                        snippet = modified_json_data[i]['abstract'].lower()
                                        if (simplified_one in snippet or simplified_two in snippet):
                                                # print(snippet)
                                                # print(json_data[i]['abstract'])
                                                sentences = snippet.split(".")
                                                for j in range(len(sentences)):
                                                        if (simplified_one in sentences[j] or simplified_two in sentences[j]):
                                                                snippets.append(json_data[i]['abstract'].split(".")[j] + ".")
                                        
                # searching regular json file
                else:
                        json_data = json.load(json_file)
                        # simplify words down into lemmmas, so that the words can be found
                        
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
        
        # response = GoogleSearch().search(word_one + " " + word_two)
        # for result in response.results:
        #         print("Title: " + result.title)
        #         print("Content: " + result.getText())
        
        page = requests.get(google_query).text
        soup = BeautifulSoup(page, "html.parser").select(".s3v9rd.AP7Wnd")
        for item in soup:
                snippets.add(item.getText(strip=True))
                        
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


