from flask import Flask, render_template, jsonify, request
from getTrendSentiment import getTrendSentiment

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
@app.route('/trends',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')

    if request.method=='POST':
        count=int(request.form.get('count'))
        trends_sentiment=getTrendSentiment(no_of_tweets=count)
        return jsonify(trends_sentiment)

if __name__ == "__main__":
    app.run(debug=True)