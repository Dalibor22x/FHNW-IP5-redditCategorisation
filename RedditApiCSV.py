import praw
import sys
import unicodecsv as csv

reddit = praw.Reddit(client_id='QS278a4Z1eWFBw',
                     client_secret='xvA8ljlQX6sV_sg2TBtTHsjcRd8',
                     user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')


def save_subreddit(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)

    with open('./subreddits/' + subreddit_name + '.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['title', 'selftext', 'score', 'id', 'url'])

        for submission in subreddit.hot(limit=limit):
            if not submission.stickied:
                writer.writerow([submission.title, submission.selftext, submission.score, submission.id, submission.url])

    print('Finished subreddit: ' + subreddit_name)

def main():
    subreddits = [
        'whatsapp',
        'spotify',
        'instagram',
        'youtube',
        'google',
        'maps',
        'snapchat',
        'netflix',
        'facebook',
        'tinder',
        'photoshop',
        'AdobeIllustrator',
        'indesign',
        'premiere',
        'MicrosoftWord',
        'excel',
        'powerpoint',
        'Slack',
        'chrome',
        'firefox',
        'Safari',
        'skype',
        'Steam'
    ]

    for subreddit in subreddits:
        save_subreddit(subreddit, 100)


if __name__ == '__main__':
    sys.exit(main())


