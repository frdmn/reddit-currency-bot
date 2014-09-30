#!/usr/bin/python

""""
Reddit currency converter bot 1.0.0

http://github.com/frdmn/reddit-currency-converter
"""

# Import modules
import time
import praw
from pprint import pprint # @TODO: remove this!

# Import settings file
import settings

# Set user agent
user_agent = ("Currency converter bot 1.0.0 by /u/frdmn "
            "github.com/frdmn/reddit-currency-bot/")

# Connect to Reddit API
r = praw.Reddit(user_agent=user_agent)

# Log in
r.login(settings.bot_username, settings.bot_password)

# Arrays to store processed items
processed_comments = []

# Infinite loop
while True:
    # Select subreddit to observe
    subreddit = r.get_subreddit(settings.observed_subreddits)
    # Loop through the hottest 10 submissions
    for submission in subreddit.get_hot(limit=10):
        # Remove hierachy and loop through them
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            # Skip if no 'body' attribute
            if not hasattr(comment, 'body'):
                continue
            # If comment isn't already processed
            if comment.id not in processed_comments:
                # Check for match
                found_currency = any(string in comment.body for string in settings.currency_keywords)
                if found_currency:
                    # Send console output
                    msg = '[Currency bot](%s)' % comment.permalink
                    # r.send_message('frdmn', 'PRAW Thread', msg)
                    print msg
                    # Add to array so we don't process this comment again
                    processed_comments.append(comment.id)
    time.sleep(1800)
