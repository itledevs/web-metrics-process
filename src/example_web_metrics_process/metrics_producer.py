from datetime import datetime
import time

# pip3 install web-metrics-process
import web_metrics_process as wmp


metrics = wmp.WebMetrics(interface='127.0.0.1', port=8001, web_path='/metrics')
metrics.start()

# metrics.data is a shared dict, beetwen your main process and the web metrics process
# you can put any key/data there, for eaxample let's update name
metrics.data['name'] = 'metrics_producer'


# you could open another web metrics instances as many as you want (just with different port)
metrics2 = wmp.WebMetrics(interface='127.0.0.1', port=8002, web_path='/metrics2', time_alive_interval_max=20)
metrics2.start()
metrics2.data['name'] = 'metrics_producer2'


# python service example, as simple as possible, infinite loop
iteration = 1
while True:
    # ... do some useful work
    
    # update metrics during the work
    metrics.data['iteration'] = iteration
    metrics.data['data'] = wmp.get_random_str()
    metrics.update_time_alive()
    print('[TRACE]', metrics.data)

    # update the second metrics instance
    metrics2.data['iteration'] = iteration
    metrics2.data['data'] = wmp.get_random_str()
    # simulate rare updates of time_alive_last, for example if main process is busy too long or hanged and there are no updates of time_alive_last
    # time_alive_ok will be False if time_alive_interval_max is exceeded, True otherwise (or None if not used)
    if iteration % 10 in (1,2,3):
        metrics2.update_time_alive()
    print('[TRACE2]', metrics2.data)

    time.sleep(10)
    iteration += 1