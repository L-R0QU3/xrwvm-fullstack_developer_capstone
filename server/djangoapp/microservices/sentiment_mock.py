from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()


@app.route('/analyze/<text>')
def analyze(text):
    score = sia.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return {'sentiment': sentiment}


if __name__ == '__main__':
    app.run(port=5000)
