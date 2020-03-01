from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify
from libbgg.apiv2 import BGG

from report import sell_report


app = Flask(__name__)
app.bgg = BGG()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/sellreport/u/<username>')
def generate_sell_report(username):
    oneyearago = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')
    report_text = sell_report(username, since=oneyearago)
    return jsonify(dict(report=report_text))


if __name__ == '__main__':
    app.run()
