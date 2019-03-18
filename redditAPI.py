import praw

reddit = praw.Reddit(client_id='QS278a4Z1eWFBw',
                     client_secret='xvA8ljlQX6sV_sg2TBtTHsjcRd8',
                     user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')


subreddit = reddit.subreddit('netflix')

# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
	#print('--------------')
    #print(submission.title)  # Output: the submission's title
    #print(submission.score)  # Output: the submission's score
    #print(submission.id)     # Output: the submission's ID
    #print(submission.url)    # Output: the URL the submission points to
    #print(submission.comments)
    #print('--------------')  # or the submission's URL if it's a self post
	for top_level_comment in submission.comments:
	    print(top_level_comment.body)
	    print('--------------')