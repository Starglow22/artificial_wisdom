# Alan Watts twitter bot

This is a modification on [tommeagher's heroku_ebooks](https://github.com/tommeagher/heroku_ebooks) repo, a Python port of [@harrisj's](https://twitter.com/harrisj) [iron_ebooks](https://github.com/harrisj/iron_ebooks/) Ruby script. 

I modified it to create more coherent text by using a weighted Markov chain rather than the basic one provided and removing the operations designed to introduce nonsense, and to source its data from a pre-collected corpus of scraped data, which I chose to collect from [this library of Alan Watts transcripts.](https://www.organism.earth/library/author/10)

I wanted to experiment with web scraping, text processing and setting up web hosted applications I suppose, and this was an interesting first foray!
