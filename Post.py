class Post(object):

    def __init__(self, title, selftext, score, id, url, all_comments):
        self.title = title
        self.selftext = selftext
        self.score = score
        self.id = id
        self.url = url
        self.comments = self.init_comments(self, all_comments)

    def init_comments(self, all_comments):
        sorted_comments = sorted(all_comments, key=lambda comment: comment.depth)



        return all_comments

    def __call__(self):
        pass