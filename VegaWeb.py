from flask import Flask

app = Flask(__name__)
from flask import render_template
# from mandrill import drill

@app.route('/')
def index():
    output = render_template('index.html')
    return output


app.run(debug=True,host='0.0.0.0',port=1900,threaded=True)

