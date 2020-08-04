import time

# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

import redis
from flask import Flask, render_template
from flask_socketio import SocketIO
import jinja2

from stuff_practice.core import config as cfg
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
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def get_count_page():
    hit_count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(hit_count)


@app.route('/t/')
def get_template():
    hit_count = get_hit_count()
    template_values = {'hit_count' : hit_count}
    template = jinja_environment.get_template('session.html')
    return template.render(template_values)


def messageReceived(methods=['GET', 'POST']):
    print('message was received')


@socketio.on('an_event')
def handle_custom_event(json, methods=['GET', 'POST']):
    print('received event with json: ' +str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
