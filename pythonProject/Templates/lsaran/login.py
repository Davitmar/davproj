from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
import json

app1 = Flask(__name__)

# with open('data.json', 'r') as data:
#     l = json.load(data)


@app1.route('/')
def log():
    if not request.args.get('username') or not request.args.get('pass'):
        return 'there are not results'
        return render_template('index1.html', l=search)
    return render_template('index1.html', l=l)



@app1.route('/post/<id>')
def read_more(id=None):
    return render_template('read_more.html', read_post=l[int(id)])


if __name__ == '__main__':
    app1.run(debug=True)

# inputi parametry inchia nstum url um ? nshanov????????
