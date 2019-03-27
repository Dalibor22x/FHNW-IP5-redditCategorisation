from datetime import datetime, timezone
from time import sleep

import praw
import sys
import csv

reddit = praw.Reddit(client_id='QS278a4Z1eWFBw',
                     client_secret='xvA8ljlQX6sV_sg2TBtTHsjcRd8',
                     user_agent='Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')


# Hard limit is no matter what 1000
def save_subreddit(subreddit_name, time_start, time_end, limit=None):
    subreddit = reddit.subreddit(subreddit_name)

    listattributes = [
        # 'author_name',
        # 'author_comment_karma',
        # 'author_has_verified_email',
        # 'author_id',
        'created_utc',
        'id',
        'is_self',
        'locked',
        'name',
        'num_comments',
        'score',
        'selftext',
        'title',
        'url'
    ]

    with open('./subreddits/' + subreddit_name + '.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(listattributes)



        for submission in subreddit.hot(limit=limit):
            if not submission.stickied:
                if time_end.timestamp() < submission.created_utc < time_start.timestamp():
                    # Check these in case author has been deleted in the mean time
                    # if not submission.author.name:
                    #     author_name = submission.author.name
                    # else:
                    #     author_name = 'johndoe'
                    #
                    # if not submission.author.comment_karma:
                    #     author_comment_karma = str(submission.author.comment_karma)
                    # else:
                    #     author_comment_karma = '0'
                    #
                    # if not submission.author.has_verified_email:
                    #     author_verified_email = str(submission.author.has_verified_email)
                    # else:
                    #     author_verified_email = 'false'
                    #
                    # if not submission.author.id:
                    #     author_id = submission.author.id
                    # else:
                    #     author_id = '0'

                    writer.writerow([
                        # author_name,
                        # author_comment_karma,
                        # author_verified_email,
                        # author_id,
                        str(submission.created_utc),
                        str(submission.id),
                        str(submission.is_self),
                        str(submission.locked),
                        submission.name,
                        str(submission.num_comments),
                        str(submission.score),
                        submission.selftext.replace("\n", ""),
                        submission.title,
                        # str(submission.upvote_ratio),
                        submission.url,
                    ])
                if submission.created_utc < time_end.timestamp():
                    break

                # sleep(0.002)

    print(('Finished subreddit: ' + subreddit_name))


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

    time_start = datetime(2019, 3, 25, 0, 0, 0, 0, tzinfo=timezone.utc)
    time_end = datetime(2019, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)

    for subreddit in subreddits:
        print("Start getting Subreddit: " + subreddit)
        save_subreddit(subreddit, time_start, time_end)


if __name__ == '__main__':
    sys.exit(main())


