import parse
import raven


LOG_TYPES = {
    'HAPROXY': [
        '{ip}:{port:d}',
        '[{time:get_time_haproxy}]',
        '{frontend_name_transport}',
        '{backend_name}/{server_name}',
        '{tq:d}/{tw:d}/{tc:d}/{tr:d}/{tt:d}',
        '{status_code:d}',
        '{bytes_sent:d}',
        '{captured_request_cookie}',
        '{captured_response_cookie}',
        '{country}',
        '{actconn:d}/{feconn:d}/{beconn:d}/{srv_conn:d}/{retries:d}',
        '{srv_queue:d}/{backend_queue:d}',
        '{{{other}}} "{http_request}"',
    ],

    'LIGHTTPD': [
        '{ip}',
        '[{time:th}]',
        '"{http_request}"',
        '{status_code:d}',
        '{byte_sent:d}',
        '"{referer}"',
        '"{user_agent}"',
        '{byte_in:d}',
        '{byte_out:d}',
        '{time_used:d}',
        '{request_hostname}',
    ],


    'NGINX': [
        '{ip}',
        '{http_x_forwarded_for}',
        '[{time:ti}]',
        '{http_host}',
        '"{http_request}"',
        '{status_code:d}',
        '{bytes_sent:d}',
        '"{http_referer}"',
        '{http_user_agentt}',
    ],

    'ATS': [
        '{time:get_time_ats} RESPONSE: sent',
        '{ip} status',
        '{status_code:d}',
        '({accelerator}) for',
        "'{http_referer}'",
    ],

    'HAPROXY2': [
        '{ip}:{port:d}',
        '[{time:get_time_haproxy}]',
        '{frontend_name_transport}',
        '{backend_name}/{server_name}',
        '{tq:d}/{tw:d}/{tc:d}/{tr:d}/{tt:d}',
        '{status_code:d}',
        '{bytes_sent:d}',
        '{captured_request_cookie}',
        '{captured_response_cookie}',
        '{country}',
        '{actconn:d}/{feconn:d}/{beconn:d}/{srv_conn:d}/{retries:d}',
        '{srv_queue:d}/{backend_queue:d}',
        '"{http_request}"',
    ]
}


def get_time_haproxy(string_time):

    return parse.datetime.strptime(string_time, "%d/%b/%Y:%H:%M:%S.%f")


def get_time_ats(string_time):

    return parse.datetime.strptime(string_time, "%Y%m%d.%Hh%Mm%Ss")


def detect_log_type(line):

    for TYPE in LOG_TYPES:
        log_format = " ".join(LOG_TYPES[TYPE])
        if TYPE == 'HAPROXY' or TYPE == 'HAPROXY2':
            error_info = parse.parse(log_format, line,
                                     dict(get_time_haproxy=get_time_haproxy))
        elif TYPE == 'ATS':
            error_info = parse.parse(log_format, line,
                                     dict(get_time_ats=get_time_ats))
        else:
            error_info = parse.parse(log_format, line)

        if error_info:
            return TYPE, log_format

    raise Exception("Unknown log type \n" + line)


def parse_log(line, log_type, log_format):

    if log_type == 'HAPROXY' or log_type == 'HAPROXY2':
        error_info = parse.parse(log_format, line,
                                 dict(get_time_haproxy=get_time_haproxy))
    elif log_type == 'ATS':
        error_info = parse.parse(log_format, line,
                                 dict(get_time_ats=get_time_ats))
    else:
        error_info = parse.parse(log_format, line)

    if error_info:
        return error_info.named
    elif log_type == 'HAPROXY':
        return parse_log(line, 'HAPROXY2', " ".join(LOG_TYPES['HAPROXY2']))
    elif log_type == 'HAPROXY2':
        return parse_log(line, 'HAPROXY', " ".join(LOG_TYPES['HAPROXY']))
    else:
        raise Exception("Unknown log type \n" + line)
