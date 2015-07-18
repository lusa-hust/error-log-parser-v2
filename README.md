# Error Log Parser V2

[![parse ver 1.6.6](https://img.shields.io/badge/parse-1.6.6-yellow.svg)](https://pypi.python.org/pypi/parse/1.6.6)
[![raven ver 5.4.1](https://img.shields.io/badge/raven-5.4.1-red.svg)](https://pypi.python.org/pypi/raven/5.4.1)
[![wheel ver 0.24.0](https://img.shields.io/badge/wheel-0.24.0-orange.svg)](https://pypi.python.org/pypi/wheel/0.24.0)

## Summary
Parsing information from HAProxy, lighttpd, nginx, ATS log files
Check Status code and send to sentry if status code is 502 or 503
## Project structure
### Module resume
* Function check_cached: Check cached if file input has cached
* Function save_to_cached: Save location by bytes of end of file log
* Function get_last_location: Get last location for resume parse log

### Module parser
* Function parse_log: parse log files and return a dict of error information
* Function detect_log_type: Get log type
* Function get_time_ats: return datetime type for time type of ats log
* Function get_time_haproxy: return datetime type for time type of haproxy log

### Module main
Open log files to gather error information
Initialize connection and push data to sentry server

## How to use
### Install dependencies
Install dependencies package from file requirements.txt
```
pip install -r requirements.txt
```
### Use
```
python main.py [option] [file-log]
```
option -r : for resume file

End document.
