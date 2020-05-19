from json import dumps

from flask import Flask

app = Flask(__name__)


@app.route('/message')
def index():
    return dumps({"message": "w00t_v2"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
