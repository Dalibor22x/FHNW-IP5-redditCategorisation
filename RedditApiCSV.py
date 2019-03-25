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
        'edited',
        'id',
        'is_self',
        'locked',
        'name',
        'num_comments',
        'over_18',
        'permalink',
        'score',
        'selftext',
        'spoiler',
        'title',
        # 'upvote_ratio',
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
                        str(submission.edited),
                        str(submission.id),
                        str(submission.is_self),
                        str(submission.locked),
                        submission.name,
                        str(submission.num_comments),
                        str(submission.over_18),
                        submission.permalink,
                        str(submission.score),
                        submission.selftext.replace("\n", ""),
                        str(submission.spoiler),
                        submission.title,
                        # str(submission.upvote_ratio),
                        submission.url,
                    ])
                if submission.created_utc < time_end.timestamp():
                    break

                # sleep(0.002)

    print(('Finished subreddit: ' + subreddit_name))

'''
Attribute	Description
author	Provides an instance of Redditor.
    Redditor:
    comment_karma	The comment karma for the Redditor.
    comments	Provide an instance of SubListing for comment access.
    created_utc	Time the account was created, represented in Unix Time.
    has_verified_email	Whether or not the Redditor has verified their email.
    icon_img	The url of the Redditors’ avatar.
    id	The ID of the Redditor.
    is_employee	Whether or not the Redditor is a Reddit employee.
    is_friend	Whether or not the Redditor is friends with the authenticated user.
    is_mod	Whether or not the Redditor mods any subreddits.
    is_gold	Whether or not the Redditor has active gold status.
    link_karma	The link karma for the Redditor.
    name	The Redditor’s username.
    subreddit	If the Redditor has created a user-subreddit, provides a dictionary of additional attributes. See below.
    subreddit['banner_img']	The URL of the user-subreddit banner.
    subreddit['name']	The fullname of the user-subreddit.
    subreddit['over_18']	Whether or not the user-subreddit is NSFW.
    subreddit['public_description']	The public description of the user- subreddit.
    subreddit['subscribers']	The number of users subscribed to the user-subreddit.
    subreddit['title']	The title of the user-subreddit.
clicked	Whether or not the submission has been clicked by the client.
comments	Provides an instance of CommentForest.
created_utc	Time the submission was created, represented in Unix Time.
distinguished	Whether or not the submission is distinguished.
edited	Whether or not the submission has been edited.
id	ID of the submission.
is_self	Whether or not the submission is a selfpost (text-only).
link_flair_template_id	The link flair’s ID, or None if not flaired.
link_flair_text	The link flair’s text content, or None if not flaired.
locked	Whether or not the submission has been locked.
name	Fullname of the submission.
num_comments	The number of comments on the submission.
over_18	Whether or not the submission has been marked as NSFW.
permalink	A permalink for the submission.
score	The number of upvotes for the submission.
selftext	The submissions’ selftext - an empty string if a link post.
spoiler	Whether or not the submission has been marked as a spoiler.
stickied	Whether or not the submission is stickied.
subreddit	Provides an instance of Subreddit.
title	The title of the submission.
upvote_ratio	The percentage of upvotes from all votes on the submission.
url The URL the submission links to, or the permalink if a selfpost.
'''


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


