#!/usr/bin/env bash

tweets_loc="`pwd`/data-gen/tweets.txt"
ft1_loc="`pwd`/tweet_input/ft1.txt"
ft2_loc="`pwd`/tweet_input/ft2.txt"

python src/tweets_cleaned.py $tweets_loc $ft1_loc
python src/average_degree.py $ft1_loc $ft2_loc