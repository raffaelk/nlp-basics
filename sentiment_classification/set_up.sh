#!/bin/bash

# get the movie reviews
curl -O http://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz
mkdir review_polarity
tar -xzf review_polarity.tar.gz -C ./review_polarity

# get opinion lexicon
curl -O -L http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar
unrar x opinion-lexicon-English.rar
mv opinion-lexicon-English opinion_lexicon

# delete archives
rm review_polarity.tar.gz
rm opinion-lexicon-English.rar

