from flask import Flask

app = Flask("dice")

@app.route('/')
def hello_world():
    return 'Hello, World!'
