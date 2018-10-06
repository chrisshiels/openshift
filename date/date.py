import datetime
import json


import flask


app = flask.Flask(__name__)


@app.route('/date')
def date():
  dt = datetime.datetime.now()
  message = json.dumps({
                         'year': dt.year,
                         'month': dt.month,
                         'day': dt.day
                       }, indent = 2) + '\n'
  return ( message, 200, { 'Content-Type': 'text/json' } )
