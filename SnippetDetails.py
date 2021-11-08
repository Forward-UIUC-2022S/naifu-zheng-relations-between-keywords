class SnippetDetails:

    # can store individual details
    string = ""
    score = 0

    def __init__(self, string):
        self.string = string

    def __lt__(self, other):
         return self.score < other.score
    