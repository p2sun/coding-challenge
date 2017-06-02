import re
import os
import sys
from dateutil import parser

# get the ft1.txt and ft2.txt locations from the command line
args = sys.argv
ft1_loc = args[1]
ft2_loc = args[2]

# Represent the Graph as an Adjacency List
# Each entry is a key value pair, the key is the hashtag, the value is a set of unique hashtags
# the current hashtag is connected to
adjacenyList = dict()
# Counter for the total number of degrees in the graph
totalDegrees = 0
# Counter for the total number of unique hash tags
uniqueHashtags = 0

# Global Queue that keeps track of every insertion into our graph
# each insertion consists of the hashtag node, the added hashtag edges and timestamp of when the tweet was generated
# EACH ENTRY consists of the timestamp, the hashtag, and a list of connected hashtags
tweets = []

#regular expressions used to extract the timestamp and hashtags from the input string
timestamp_regex = '[A-Z,a-z]{3} [A-Z,a-z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \+[0-9]{4} [0-9]{4}'
hashtag_regex = '\S*#(?:\[[^\]]+\]|\S+)'


#     Use this helper function to remove tweets from our adjacency list graph and tweets list that are
#     more than a minute old compared to the most recent tweet
#
#     @param timestamp Timestamp of the most recent tweet.
#     @return a two integers: the number of old hashtags and the number of graph edges that were removed from our
#               adjacency list graph
#
def removeOldTweets(timestamp):
    oldHashtags = 0
    oldConnections = 0
    # iterate through all the tweets we currently are tracking
    # if the time difference is greater than 60 seconds, pop it from the list
    # Get the hashtag and its edges and remove all the edges that
    # are found in our adjacency list
    for tweet in tweets:
        #take the time difference
        timeDiff = tweet[0] - timestamp
        #if the time difference is more than 60 seconds, remove the hashtag and connections
        if timeDiff.seconds > 60:
            #remove the transaction from tweets queue
            tweets.pop()
            hashtag = tweet[1]
            connectedHashtags = tweet[2]
            # each entry in the adjacencyList is a key value pair, the key is the hashtag
            # the value is a list of all the hashtags that have connections
            # do a list subtraction to remove all the old connections we want to get rid of
            adjacenyList[hashtag] -= connectedHashtags
            # if there are no connections in that list, there is one less node in our graph
            # increment the oldHashtag counter
            if adjacenyList[hashtag].__len__() == 0:
                oldHashtags += 1
            # increment our old edges counter, by the number of connections we've removed
            oldConnections += connectedHashtags.__len__()
        else:
            # our Queue is FIFO, so if we've reached a point where a transaction is within our time bound
            # we know that every entry after this point is more recent, so we can stop going through our queue
            # break away from out for list iteration
            break
    return oldHashtags, oldConnections


# open ft2 and write to it as we go along, we'll close it at the end
ft2 = open(ft2_loc, 'w')

# open ft1 to processed our cleaned tweets
with open(ft1_loc, 'r') as ft1:
    for line in ft1:
        # Don't process the last line which gives the number of tweets that contained unicode
        if line.__contains__('contained unicode') == False:
            #extract the hashtags from the string using our regex
            hashtags = set(re.findall(hashtag_regex, line))
            #extract the timestamp from the string using our regex
            timestamp = re.findall(timestamp_regex, line)
            # if there exists a timestamp and a list of hashtags, process the tweet
            if timestamp.__len__() > 0 and hashtags.__len__() > 0:

                #get the time of the timestamp, that is the most recent time
                currentTime = parser.parse(timestamp[0])

                #-----------REMOVE OLD TWEETS ------------------------------
                # remove old tweets from our graph
                [oldHashtags, oldConnections] = removeOldTweets(currentTime)
                #decrease our counter for the number of nodes in our graph
                uniqueHashtags = max(0, uniqueHashtags - oldHashtags)
                #decrease our counter for the number of edges in our graph
                totalDegrees -= oldConnections
                #-----------------------------------------------------------

                #----------UPDATE OUR CURRENT NODE AND EDGES COUNTERS-------
                # increment the total number of degrees in our graph by the number of connections
                numberOf_hashtags = hashtags.__len__()
                totalDegrees += ( numberOf_hashtags - 1) * numberOf_hashtags
                #-----------------------------------------------------------

                #---------UPDATE OUR ADJACENCY LIST TO REFLECT NEW EDGES----
                #iterate through each hashtag in the list
                for hashtag in hashtags:
                    # get all the other hashtags that the current hashtag is connected to
                    connectedHashtags = hashtags.difference([hashtag])
                    # add to our tweet queue to update when this tweet was added to our tweet graph
                    tweets.append([currentTime, hashtag, connectedHashtags])

                    if hashtag in adjacenyList:
                        # merge the two sets of hashtags, the new connections and old connections
                        adjacentTags = adjacenyList[hashtag]
                        adjacentTags.update(connectedHashtags)
                        # update the entry in the adjacency list graph with the new set
                        adjacenyList[hashtag] = adjacentTags
                    else:
                        # if the hashtag isn't in the adjacency list, then add an entry and increment
                        # the total number of unique hashtags by 1
                        adjacenyList[hashtag] = connectedHashtags
                        uniqueHashtags += 1
                #-----------------------------------------------------------

                #-------FORMAT OUR OUTPUT STRING FOR THIS TWEET NEW-------------
                if uniqueHashtags != 0:
                    outputString = '{:.2f}'.format(float(totalDegrees) / uniqueHashtags)
                # ---- if unique hashtags is 0, then the output string should just be zero
                # ---- no divide by zero
                else:
                    outputString = '0.00'
            else:
                if uniqueHashtags != 0:
                    averageDegree = float(totalDegrees) / uniqueHashtags
                    outputString = '{:.2f}'.format(averageDegree)

                # ---- if unique hashtags is 0, then the output string should just be zero
                # ---- no divide by zero
                else:
                    outputString = '0.00'

            #-----WRITE THE OUTPUT STRING TO OUR OUTPUT FILE------------------------
            ft2.write(outputString + '\n')

#close ft2
ft2.close()





