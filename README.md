### web-metrics-process
easy way to add web metrics to python daemon. Update metrics from main logic in dict shared to additional python web process
this is designed for linux production systems (you could get issues with spawn process on mac)


```
# install
# pip3 install web-metrics-process
import web_metrics_process as wmp


metrics = wmp.WebMetrics(interface='127.0.0.1', port=8001, web_path='/metrics')
metrics.start()

# metrics.data is a shared dict, beetwen your main process and the web metrics process
# you can put any key/data there, for eaxample let's update name
metrics.data['name'] = 'metrics_producer'
metrics.data['name'] = 'something you want'

# there are already some service fields for convinience
# time_started - start time of python service
# time_alive_last - in each iteration of processing of something you could update alive time to watch by metric is something hanged or waiting resourses or not 
 metrics.update_time_alive()

```

### get metrics by browser or any tool
```
curl -s http://127.0.0.1:8001/metrics | jq .
{
  "time_started": "2026-06-03T14:03:47.397088",
  "time_alive_last": "2026-06-03T14:03:47.583579",
  "time_alive_interval_max": 0,
  "time_alive_ok": null,
  "iteration": 17,
  "name": "metrics_producer",
  "version": null,
  "session_id": "huCfS1YH",
  "data": "something you want"
}
```


### Example is here (simple service based on infinite loop):
src/example_web_metrics_process/metrics_producer.py
