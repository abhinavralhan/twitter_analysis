import sys
from collections import Counter
import json

def get_media(tweet):
    entities = tweet.get('entities', {})
    media = entities.get('media', [])
    return media

if __name__ == '__main__':
    file = open('textimage.csv', 'w')
    fname = sys.argv[1]
    i=0
    with open(fname, 'r') as f:
        counttext = 0
        countimage = 0

        for line in f:
            tweet = json.loads(line)
            media_in_tweet = get_media(tweet)

            if media_in_tweet:
                countimage += 1

            text = tweet.get('text', {})
            if text:
                counttext += 1

    #print("{}, {}".format(counttext, countimage))
    file.close()

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('username', 'api_key')
trace1 = {
  "x": ["Text", "Image", "Text + Image"], 
  "y": ["13728", "1161", "1090"], 
  "marker": {
    "color": "rgb(158,202,225)", 
    "line": {
      "color": "rgb(8,48,107)", 
      "width": 1.5
    }
  }, 
  "name": "y", 
  "opacity": 0.6, 
  "text": ["13728", "1161", "1090"], 
  "textsrc": "abhinavralhan:0:5dbb51", 
  "type": "bar", 
  "uid": "0b99d5", 
  "xsrc": "abhinavralhan:0:e2009f", 
  "ysrc": "abhinavralhan:0:a8faa7"
}
data = Data([trace1])
layout = {
  "hovermode": "x", 
  "title": "Comparison of Tweets", 
  "xaxis": {
    "autorange": True, 
    "range": [-0.5, 2.5], 
    "title": "Type of Tweet", 
    "type": "category"
  }, 
  "yaxis": {
    "autorange": True, 
    "range": [0, 14450.5263158], 
    "title": "Count", 
    "type": "linear"
  }
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)