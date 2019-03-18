class Comment:

    def __init__(self, id, parent_id, body):
        self.id = id
        self.parent_Id = parent_id
        self.body = body
        self.comments = []

    def add_comment(self, comment):
        self.comments.__add__(self, comment)