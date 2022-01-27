import FindRelationship
import SnippetDetails
import json
import sys

DATA_DIR = "/Users/ashutoshukey/Downloads/Forward_Data_Lab/Code/data/Papers"

PAPERS_FILE = f"{DATA_DIR}/filtered_arxiv.json"
PAPERS_LEMMA_FILE = f"{DATA_DIR}/filtered_arxiv_lemmatized.json"

# FindRelationship.LemmatizeEntireFile(PAPERS_FILE, PAPERS_LEMMA_FILE)
# FindRelationship.FindRelationshipJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json")
#FindRelationship.FindRelationshipModifiedJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/filtered_arxiv_lemmatized.json")
#FindRelationship.SearchGoogle("Btree", "Data Structure")

if __name__ == "__main__":
    keyword = sys.argv[1]
    q_keyword = sys.argv[2]

    res = FindRelationship.FindRelationshipModifiedJson("Tree", "Data Structure", PAPERS_FILE, PAPERS_LEMMA_FILE)
    # res = FindRelationship.FindRelationshipModifiedJson(keyword, q_keyword, PAPERS_FILE, PAPERS_LEMMA_FILE)

    # print(json.dumps(res, indent=4))
    # with open("yo-debug.log", "w") as f:
    #     f.write(keyword + '\n')
    #     f.write(q_keyword + '\n')
    #     f.write(json.dumps(res, indent = 4))

    print(json.dumps(res))
