# Error Log Parser V2

[![parse ver 1.6.6](https://img.shields.io/badge/parse-1.6.6-yellow.svg)](https://pypi.python.org/pypi/parse/1.6.6)
[![raven ver 5.4.1](https://img.shields.io/badge/raven-5.4.1-red.svg)](https://pypi.python.org/pypi/raven/5.4.1)
[![wheel ver 0.24.0](https://img.shields.io/badge/wheel-0.24.0-orange.svg)](https://pypi.python.org/pypi/wheel/0.24.0)

## Summary
Parsing information from HAProxy, lighttpd, nginx, ATS log files
Check Status code and send to sentry if status code is 502 or 503
## Project structure
### Module parsers
* Function build_log_format: create a formatting string to parse log files
* Function parse_log_file: parse log files and return a dict of error information

### Module name
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
python main.py [file-log]
```
