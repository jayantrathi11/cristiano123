from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def first():
    return render_template('submit.html')

@app.route('/capitalize', methods=['POST', 'GET'])
def capital():
    temp = request.form['temp']
    return render_template('index.html', new_name = temp.upper())


if name == '__main__':
    app.run()