__author__ = 'li'

import parse
import raven



LOG_TYPES = {
    'HAPROXY': [
        '{ip}:{port} ',
        '[{times}] ',
        '{frontend_name_transport} ',
        '{backend_name}/{server_name} ',
        '{tq}/{tw}/{tc}/{tr}/{tt} ',
        '{status_code} ',
        '{bytes_sent} ',
        '{captured_request_cookie} ',
        '{captured_response_cookie} ',
        '{country} ',
        '{actconn}/{feconn}/{beconn}/{srv_conn}/{retries} ',
        '{srv_queue}/{backend_queue} ',
        '{{{other}}} "{http_request}"',
    ],

    'LIGHTTPD': [
        '{ip} ',
        '[{time}] ',
        '"{http_request}" ',
        '{status_code} ',
        '{byte_sent} ',
        '"{referer}" ',
        '"{user_agent}" ',
        '{byte_in} ',
        '{byte_out} ',
        '{time_used} ',
        '{request_hostname}"',
    ],

    'NGINX': [
        '{ip} ',
        '{http_x_forwarded_for} ',
        '[{time}] ',
        '{http_host} ',
        '"{http_request}" ',
        '{status_code} ',
        '{bytes_sent} ',
        '"{http_referer}" ',
        '{http_user_agentt}',
    ],

    'ATS': [
        '{time} RESPONSE: sent ',
        '{ip} status ',
        '{status_code} ',
        '({accelerator}) for ',
        "'{http_referer}'",
    ],

    'HAPROXY2': [
        '{ip}:{port} ',
        '[{times}] ',
        '{frontend_name_transport} ',
        '{backend_name}/{server_name} ',
        '{tq}/{tw}/{tc}/{tr}/{tt} ',
        '{status_code} ',
        '{bytes_sent} ',
        '{captured_request_cookie} ',
        '{captured_response_cookie} ',
        '{country} ',
        '{actconn}/{feconn}/{beconn}/{srv_conn}/{retries} ',
        '{srv_queue}/{backend_queue} ',
        '"{http_request}"',
    ]
}


def build_log_format(log_type):
    log_format = ""

    for field in log_type:
        log_format += field

    return log_format


def parse_log(line):
    for TYPE in LOG_TYPES:
        log_format = build_log_format(LOG_TYPES[TYPE])
        error_info = parse.parse(log_format, line)

        if error_info:
            return error_info.named

    raise "Unknown log type", line