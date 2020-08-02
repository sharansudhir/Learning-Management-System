from flask import Flask, send_file, request
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)


def get_entities(raw_words):
    data = raw_words.strip().split(" ")
    words = []
    for word in data:
        if len(word) > 0 and word[0].isupper():
            word = ''.join(char for char in word if char.isalnum())
            words.append(word)
    return ' '.join(word for word in words)


@app.route('/', methods=['POST'])
def hello_world():
    data = get_entities(request.form['data'])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=1500,
                          height=1500
                          ).generate(data)
    wordcloud.to_file("static/wordcloud.png")
    return send_file('static/wordcloud.png')


if __name__ == '__main__':
    app.run()