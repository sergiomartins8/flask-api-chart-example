from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/message/<message_id>', methods=['GET'])
def get_message(message_id):
    return jsonify({'my_message': append_id(message_id)})


def append_id(message_id):
    return f'w00t_{message_id}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
