# Movie Sentiment Pipeline

This repository implements a generic infrastructure, using message-oriented-middleware (MOM), to perform sentiment analysis on movie reviews, built as part of the course [Enterprise Application Integration](https://www.rug.nl/ocasys/fwn/vak/show?code=WMCS007-05).
This system extracts data (user reviews) from various sources (e.g. reddit, twitter, IMDB, ...), translating it into a canonical data model, after which its sentiment is extracted.
All of this data is stored in persistent storage, after which it is extracted through a web GUI.
