from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


# cors = CORS(app, resources={r"/home/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('basic.html')


@app.route('/Frontend/<path:path>')
def send_fe(path):
    return send_from_directory('Frontend', path)


@app.route('/home')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
