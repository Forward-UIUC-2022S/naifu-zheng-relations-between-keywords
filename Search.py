import en_core_web_sm
from sklearn import preprocessing
from whoosh import index, writing, qparser
import whoosh.index as index
from whoosh.index import *
from whoosh.fields import *
from whoosh.filedb.filestore import FileStorage
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.query import *
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import nltk 
from nltk import word_tokenize
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request


nlp = en_core_web_sm.load()



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
                size_to_lemma = min(50000, len(json_data))
                json_data = json_data[:size_to_lemma]
                for i in tqdm(range(size_to_lemma)):
                        # value = json_data[i]
                        json_data[i][element_to_search] = Lemmatization(json_data[i][element_to_search])
                        # lemmatized = Lemmatization(value['abstract'])
                        # to_write = {
                        #         "abstract" : lemmatized,
                        # }
                        # json.dump(to_write, output_file)
                output_file.close()
        with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(json_data))

def SearchJsonFile(word_one, word_two, json_data, modified_json_path=None, max_limit=40):
        snippets = []
        #with open(path) as json_file:
        simplified_one = Lemmatization(word_one).lower()
        simplified_two = Lemmatization(word_two).lower()
        # lemmatized json file has been initialized already
        if modified_json_path != None:
                with open(modified_json_path) as modified_json_file:
                        json_data = json.load(json_file)
                        modified_json_data = json.load(modified_json_file)
                        length = min(len(json_data), len(modified_json_data))
                        for i in range(length):
                                snippet = modified_json_data[i][element_to_search].lower()
                                if (simplified_one in snippet or simplified_two in snippet):
                                        # print(snippet)
                                        # print(json_data[i]['abstract'])
                                        sentences = snippet.split(".")
                                        for j in range(len(sentences)):
                                                if (simplified_one in sentences[j] or simplified_two in sentences[j]):
                                                        snippets.append(json_data[i][element_to_search].split(".")[j] + ".")
                                # stop after hitting max amount
                                if (len(snippets) >= max_limit):
                                        break
                                
        # searching regular json file
        else:
                #json_data = json.load(json_file)
                #simplify words down into lemmmas, so that the words can be found
                schema = Schema(id = ID(stored = True), submitter = TEXT(stored = True), authors = TEXT(stored = True), title = TEXT(stored = True), comments = TEXT(stored = True), abstract = TEXT(stored = True))
                        

                if not os.path.exists("indexdir"):
                        os.mkdir("indexdir")
                        ix = index.create_in("indexdir", schema)
                        writer = ix.writer()
                        for paper in json_data:
                                writer.add_document(id = paper["id"], title = paper["title"], abstract = paper["abstract"])
                        writer.commit()
                else:
                        ix = open_dir("indexdir")
                
                
                #search for abstracts that fit the expected path
                searcher = ix.searcher()
                proposed_time_strings = []
                with ix.searcher() as searcher:
                        parser = QueryParser("abstract", ix.schema, group=qparser.OrGroup)
                        #querystring = u"query plan"# AND(content:months OR content:weeks OR content:days OR content:hours OR content:minutes OR content:seconds)"
                        querystring = word_one + ' ' + word_two
                        myquery = parser.parse(querystring)
                        results = searcher.search(myquery, limit = 40)
                        
                        print(len(results))
                        for res in results:
                                #print(res['title'])
                                snippets.append(res["abstract"])
                                
                        

        return snippets


def SnippetPreprocess(snippetsToProcess:list):
        processedSnippets = []
        for snippet in snippetsToProcess:
                snippet = snippet.replace('\xa0', ' ')
                sentences = snippet.split(". ")
                containsDate = re.search("(Posted:)*.{4}(([0-9]{1})|([0-9]{2})), [0-9]{4}·?",snippet)
                if containsDate:
                        if containsDate.start() < 2:
                                snippet = snippet[containsDate.end():]
                        else:
                                snippet = snippet[:containsDate.start()]
                if snippet.find("...") >= 0:
                        snippet = snippet[:snippet.find('...')]

                POSlist = nltk.pos_tag(word_tokenize(snippet))
                
                for POSpair in POSlist:
                        if POSpair[1] == "VB" or POSpair[1] == "VBP" or POSpair[1] == "VBZ":
                                processedSnippets.append(snippet)
                                break
                        
                        
        return processedSnippets
        
def SearchGoogleList(word_one, word_list, deeper_web_search=False):
        snippets = []
        # replace space with + for google query
        item_one = word_one.replace(' ', '+')

        for second_word in word_list:
                snippets_sub = []
                item_two = second_word.replace(' ', '+')
                google_query = 'https://www.google.com/search?q='+item_one+'+'+item_two
        
                # getting snippets from google search
                page = requests.get(google_query)
                html_page = page.text
                # takes the snippet from the page
                soup = BeautifulSoup(html_page, "html.parser")
                snippet_soup = soup.select(".s3v9rd.AP7Wnd")
                hyper_link_soup = search(word_one + ' '+ second_word, num_results=10, lang="en")

                #print(search(word_one + ' '+ second_word, num_results=10, lang="en"))
                # for item in hyper_link_soup:
                #     print(item.getText)
                # direct snippets from google
                for item in snippet_soup:
                        # dont want repeats
                        to_add_original = item.getText(strip=True)
                        to_add = to_add_original.replace("-", "").lower()
                        if (any(to_add_original in string for string in snippets_sub)):           #case sensitive
                                # google repeated same results, ignore this item
                                continue
                        if (word_one.lower() in to_add or second_word.lower() in to_add):              #changed or to and
                                snippets_sub.append(to_add_original)
                                if (len(snippets_sub) >= 10):              #changed max_search count to 30
                                        break
                snippets.append(SnippetPreprocess(snippets_sub))
        return snippets

def SearchGoogle(word_one, word_two, deeper_web_search):
        snippets = []
        # replace space with + for google query
        item_one = word_one.replace(' ', '+')
        item_two = word_two.replace(' ', '+')
        google_query = 'https://www.google.com/search?q='+item_one+'+'+item_two
        # getting snippets from google search
        page = requests.get(google_query)
        html_page = page.text
        
        # takes the snippet from the page
        soup = BeautifulSoup(html_page, "html.parser")
        snippet_soup = soup.select(".s3v9rd.AP7Wnd")
        hyper_link_soup = search(word_one + ' '+ word_two, num_results=10, lang="en")

        # direct snippets from google
        for item in snippet_soup:
                # dont want repeats
                to_add_original = item.getText(strip=True)
                to_add = to_add_original.replace("-", "").lower()
                if (any(to_add_original in string for string in snippets)):           #case sensitive
                        # google repeated same results, ignore this item
                        continue
                if (word_one.lower() in to_add or word_two.lower() in to_add):              #changed or to and
                        snippets.append(to_add_original)
                        if (len(snippets) >= 20):              #changed max_search count to 30
                                break
        preprocessed_snippets = SnippetPreprocess(snippets)
        if not deeper_web_search:
                return preprocessed_snippets
        deep_web_snippets = []
        for snippet in preprocessed_snippets:
                if snippet[len(snippet) - 1] == '.':
                        deep_web_snippets.append(snippet)
                        continue
                for url in hyper_link_soup:
                        deep_search_result = deepSearch(url, snippet)
                        if len(deep_search_result) > 0:
                                deep_web_snippets.append(deep_search_result)
        return deep_web_snippets


def newSearch(word_one, word_two):
    query1 = word_one + " " + word_two

    query = query1.replace(' ', '+')
    google_query = 'https://www.google.com/search?q='+query
    http = httplib2.Http()
    status, response = http.request(google_query)

    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            print(link['href'])
    
    return search(query1, num_results=10, lang="en")

'''
Input: url(string), incomplete_snippet(string)
Output: (string)
Takes an URL and an incomplete_snippet as input, find the complete sentence in the
webpage of the URL.
'''
def deepSearch(url, incomplete_snippet):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for item in soup.findAll("div"):
                to_add_original = item.getText(strip=True)
                to_add = to_add_original.replace("-", "")
                tmp_incomp = incomplete_snippet.replace("-", "")
                incomplete_start_idx = to_add.find(tmp_incomp)
                end_idx = to_add[incomplete_start_idx + len(incomplete_snippet)-1:].find('.')
                if incomplete_start_idx >= 0:
                        return to_add[incomplete_start_idx: incomplete_start_idx + len(incomplete_snippet) + end_idx]
        return ""

