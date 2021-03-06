import time
import json
# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import redis
from flask import Flask, render_template
from flask_socketio import SocketIO
import jinja2

from when_the.core import config as cfg
from when_the.core.logging import logger
from when_the.nlp import nlp
#import .stuff_practice

app = Flask(__name__)
app.config['SECRET_KEY'] = cfg.app_secret_key
cache = redis.Redis(host='redis', port=6379)
socketio = SocketIO(app)
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('templates'))


def get_hit_count():
    retries = 5
    while True:
        try:
            new_count = cache.incr('hits')
            logger.info(f"Site hit. New count is {new_count}")
            return new_count
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def get_count_page():
    hit_count = get_hit_count()
    # return 'Hello World! I have been seen {} times.\n'.format(4)
    template_values = {'hit_count' : hit_count}
    template = jinja_environment.get_template('session.html')
    return template.render(template_values)


@app.route('/t/')
def get_template():
    #hit_count = get_hit_count()
    template_values = {'hit_count' : 2}
    template = jinja_environment.get_template('session.html')
    return template.render(template_values)


def messageReceived(methods=['GET', 'POST']):
    logger.info('Callback called from message emit.')


def alter_json(python_dict):
    #python_dict = json.load(json_obj)
    try: 
        user_message = python_dict['message']
        python_dict['message'] = nlp.alter_message(user_message)
    except:
        pass
    return python_dict
    #return json.dump(python_dict)


@socketio.on('my event')
def handle_custom_event(json_obj, methods=['GET', 'POST']):
    logger.info('Server received websocket event with json: ' +str(json_obj))
    altered_json = alter_json(json_obj)
    logger.info('Server will emit websocket event with json: ' +str(altered_json))
    socketio.emit('my response', altered_json, callback=messageReceived)
    return


if __name__ == '__main__':
    socketio.run(app, debug=True)
