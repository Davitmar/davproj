from flask import Flask, render_template

app=Flask(__name__)


with open('.\Templates\MOCK_DATA.csv','r') as file:
    l=file.readlines()


@app.route('/users/')
#@app.route('/users/<id>')
def index():
    return render_template('base.html', l=l)

@app.route('/users/<id>')
def id(id):
    for i in l:
        try:
            if id == i[:len(id)]:
                return f'<p>  {i}<p>'
        except:
            pass
if __name__=='__main__':
    app.run(debug=True)

#envoirmenti activate incha petqa tes che
#terminalic run anel te pycharmic nuynna te che
#aranc env klni te che
#FLASK_APP=app ??????????
#exceptov vonc ashxatel