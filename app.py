from flask import Flask, render_template, send_from_directory
from Project import app, db
from Project.models import Electives
app = Flask(__name__)


# cors = CORS(app, resources={r"/home/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Frontend/<path:path>')
def send_fe(path):
    return send_from_directory('Frontend', path)


@app.route('/home')
def hello():
    return "Hello World!"


@app.route('/list')
def openlist():
    return render_template('list.html')

@app.route('/reccomend')
def recc():
    return render_template('reccme.html')


if __name__ == '__main__':
    app.run(debug=True)
