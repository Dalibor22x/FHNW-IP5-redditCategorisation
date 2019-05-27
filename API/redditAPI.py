import praw
import sys
from API.Post import Post

reddit = praw.Reddit(client_id='QS278a4Z1eWFBw',
                     client_secret='xvA8ljlQX6sV_sg2TBtTHsjcRd8',
                     user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')


def print_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.hot(limit=limit):
        if not submission.stickied:
            print('Title: ' + submission.title)
            print('Selftext: ' + submission.selftext)
            print('Score: ' + str(submission.score))
            print('ID: ' + str(submission.id))
            # Add author
            print('URL: ' + submission.url)
            print('Comments:')
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print('Comment ID: ' + str(comment.id))
                print('Parent ID: ' + str(comment.parent_id))
                print(comment.body)
                print('Score: ' + str(comment.score))
                print('Comment Depth: ' + str(comment.depth))
                print('-------')
            print('--------------')
            print('\n\n\n')

def get_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.hot(limit=limit):
        if not submission.stickied:
            submission.comments.replace_more(limit=None)
            post = Post(submission.title, submission.selftext, submission.score, submission.id, submission.url, submission.comments.list())

def main():
    print_subreddit('netflix')
    # get_subreddit('netflix')


if __name__ == '__main__':
    sys.exit(main())
