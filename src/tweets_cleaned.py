import simplejson as json
import os
import re
import sys

args = sys.argv
tweet_loc = args[1]
ft1_loc = args[2]

#     Use this helper function to find if unicode exists in the input string
#     @param s The input string.
#     @return a boolean representing if unicode exists in the string
def ContainsUnicode(s):
    unicodeCharacters = re.match('^[\x00-\x7F]+$', s)
    return unicodeCharacters == None

output_file = open(ft1_loc, 'w')
output_string = ""
unicodeTweets = 0
# take the input tweet file and process the tweets in the file
with open(tweet_loc, 'r') as input_file:
    for line in input_file:
        tweet = json.loads(line)
        # if text entry is in the tweet, process it
        if 'text' in tweet:
            text = tweet['text']
            timestamp = tweet['created_at']
            # if it contains unicode, strip it from the text and increment our unicodeTweets counter
            if ContainsUnicode(text):
                text = text.encode('ascii', 'ignore')
                unicodeTweets += 1
            # remove all the string escape
            text = text.decode('string_escape').replace('\n', '')
            # format the string we write to file
            output_string = text + ' ( timestamp: ' + timestamp + ')\n'
            output_file.write(output_string)

# add the number of tweets containing unicode
output_string += str(unicodeTweets) + " tweets contained unicode"

output_file.close()


