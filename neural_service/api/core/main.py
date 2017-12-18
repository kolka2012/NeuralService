# -*- coding: utf-8 -*-

import config
import logging
from flask import current_app, Flask, request, jsonify
import urllib2
import base64
import json
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config.from_object(config)

logging.basicConfig(level=logging.INFO)


def fetch_predictions(img_stream):
    """Отправляем изображение в формате base64 в нейронную сеть.
    Адрес нейронной сети указан в config.py

    :param img_stream: изображение в формате base64
    :return: результат нейронной строки в формате json
    """
    predictions = {}
    server_url = current_app.config['PREDICTION_SERVICE_URL']
    req = urllib2.Request(server_url, json.dumps({'data': base64.b64encode(img_stream)}),
                          {'Content-Type': 'application/json'})
    try:
        f = urllib2.urlopen(req)
        predictions = json.loads(f.read())
    except urllib2.HTTPError as e:
        current_app.logger.exception(e)

    current_app.logger.info('Predictions: %s', predictions)
    return predictions


@app.route('/', methods=['POST'])
def main():
    try:
        data = request.get_json()
    except KeyError:
        return jsonify(status_code='400', msg='Bad Request'), 400
    url = data['url']
    img = urllib2.urlopen(url)
    response = img.info()
    if response.type in current_app.config['ALLOWED_CONTENT_TYPES']:
        img_stream = img.read()
        predictions = fetch_predictions(img_stream=img_stream)
        return jsonify(predictions=predictions)
    else:
        raise BadRequest(
            "{0} his an invalid type".format(response.type))


@app.errorhandler(500)
def server_error(e):
    current_app.logger.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)