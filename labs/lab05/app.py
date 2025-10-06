from flask import Flask
import redis
import os
import socket

app = Flask(__name__)
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def hello():
    count = redis_client.incr('hits')
    hostname = socket.gethostname()
    return f'''
    <html>
        <body>
            <h1>¡Hola desde Kubernetes!</h1>
            <p>Visita número: <strong>{count}</strong></p>
            <p>Servido por: <strong>{hostname}</strong></p>
            <p>Redis Host: <strong>{redis_host}</strong></p>
        </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
