from flask import Flask
app = Flask(__name__)
import main as prediction
@app.route('/Login')
def hello_world():
    res = prediction.getPrediction("Great for the jawbone")
    return str(res)