from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator

# from textblob import TextBlob

app = Flask(__name__)

person = {
    'first_name': '温',
    'last_name': '砚',
    'address': '湖北师范大学',
    'job': 'Python developer',
    'tel': '173********',
    'email': 'wenyanpython@outlook.com',
    'description': '在学习python后，深切感受到python的魅力，同时python在人工智能、数据挖掘、机器视觉方面的应用领域非常的广泛，所以我想谋求一份python有关的实习岗位',
    'social_media': [
        {
            'link': 'https://github.com/Wenyanlikefish',
            'icon': 'fa-github'
        }
    ],
    'img': 'img/img_nono.jpg',
    'experiences': [

    ],
    'education': [
        {
            'university': '湖北师范大学',
            'degree': '计算机与信息工程学院',
            'description': '软件工程',
            'mention': 'Bien',
            'timeframe': '2018 - 2022'
        }
    ],
    'programming_languages': {
        'Python': ['fa-python', '90'],
        'HMTL': ['fa-html5', '70'],
        'CSS': ['fa-css3-alt', '70'],
        'JS': ['fa-js-square', '70'],
        'Mongo DB': ['fa-database', '60'],
    },
    'languages': {'English': '四级', '普通话': '二乙'},
    'interests': ['旅行', '看书']
}


@app.route('/')
def cv(person=person):
    return render_template('index.html', person=person)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route('/chart')
def index():
    return render_template('chartsajax.html', graphJSON=gm())


def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/senti')
def main():
    text = ""
    values = {"positive": 0, "negative": 0, "neutral": 0}

    with open('ask_politics.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 2000 == 0:
                break
            if 'text' in row:
                nolinkstext = re.sub(
                    r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                    '', row['text'], flags=re.MULTILINE)
                text = nolinkstext

            blob = TextBlob(text)
            for sentence in blob.sentences:
                sentiment_value = sentence.sentiment.polarity
                if sentiment_value >= -0.1 and sentiment_value <= 0.1:
                    values['neutral'] += 1
                elif sentiment_value < 0:
                    values['negative'] += 1
                elif sentiment_value > 0:
                    values['positive'] += 1

    values = sorted(values.items(), key=operator.itemgetter(1))
    top_ten = list(reversed(values))
    if len(top_ten) >= 11:
        top_ten = top_ten[1:11]
    else:
        top_ten = top_ten[0:len(top_ten)]

    top_ten_list_vals = []
    top_ten_list_labels = []
    for language in top_ten:
        top_ten_list_vals.append(language[1])
        top_ten_list_labels.append(language[0])

    graph_values = [{
        'labels': top_ten_list_labels,
        'values': top_ten_list_vals,
        'type': 'pie',
        'insidetextfont': {'color': '#FFFFFF',
                           'size': '14',
                           },
        'textfont': {'color': '#FFFFFF',
                     'size': '14',
                     },
    }]

    layout = {'title': '<b>意见挖掘</b>'}

    return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
