__version__ = "2026.5.2"

from multiprocessing import Process, Manager
from fastapi import FastAPI
import uvicorn
import random
from datetime import datetime
from string import ascii_letters, digits


def get_random_str(generated_len=6):
    """Get random string of letters, digits """
    password_characters = ascii_letters + digits
    return ''.join(random.choice(password_characters) for i in range(generated_len))


def web_process(metrics_data, interface='127.0.0.1', port=8001, web_path='/metrics'):
    app = FastAPI()
    @app.get(web_path)
    def metrics():
        return metrics_data
    uvicorn.run(app, host=interface, port=port)


class WebMetrics:
    def __init__(self, interface='127.0.0.1', port=8001, web_path='/metrics'):
        self.interface = interface
        self.port = port
        self.web_path = web_path
        self.process = None

        self.data = Manager().dict() 
        self.data['time_started'] = f'{datetime.now()}'
        self.data['time_alive_last'] = None
        self.data['iteration'] = 0
        self.data['name'] = None
        self.data['version'] = None
        self.data['session_id'] = get_random_str(generated_len=8)

    def start(self, daemon=True):
        #(!) designed and valid only for linux. macOS multiprocessing is with issues, uses spawn method (forced fork got issues with uvicorn)
        self.process = Process(target=web_process, kwargs={ 'metrics_data': self.data, 'interface': self.interface, 'port': self.port, 'web_path': self.web_path }, daemon=daemon)
        self.process.start()
    
    def stop(self):
        if self.process:
            self.process.terminate()
    
    def __del__(self):
        if self.process:
            self.stop()

    def update_time_alive(self):
        self.data['time_alive_last'] = f'{datetime.now()}'



## Example of usage in code:
# from web_metrics_process import WebMetrics
# web_metrics = WebMetrics()
# web_metrics.start()

## This will be available at http://<interface>:<port>/<web_path> in JSON format, default: http://127.0.0.1:8001/metrics
# web_metrics.data['somekey'] = 'somevalue'    
