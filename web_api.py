from flask import Flask

app = Flask(__name__)


@app.get('/')
def index():
    return "<h1>ez-android-automator</h1>Web API for ez-android-automator, check api docs for more help."


@app.get('/running_client')
def get_running_client():
    return 0

def run_web_api():
    app.run(port=4778)
