import praw
import sys

reddit = praw.Reddit(client_id='QS278a4Z1eWFBw',
                     client_secret='xvA8ljlQX6sV_sg2TBtTHsjcRd8',
                     user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')


def printSubreddit(subredditName, limit=10):
    subreddit = reddit.subreddit(subredditName)

    for submission in subreddit.hot(limit=limit):
        print('Title: ' + submission.title)
        print('Selftext: ' + submission.selftext)
        print('Score: ' + str(submission.score))
        print('ID: ' + str(submission.id))
        print('URL: ' + submission.url)
        print('Comments:')
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print("Parent ID: " + str(comment.parent_id))
            print(comment.body)
            print('-------')
        print('--------------')
        print('\n\n\n')


def main():
    printSubreddit('netflix')


if __name__ == '__main__':
    sys.exit(main())
