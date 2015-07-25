import sys
import parser
import os
from pygtail import Pygtail
import raven


if __name__ == '__main__':
    # initialize connection to sentry server
    client = raven.Client(
        dsn="http://ea8723b06f824d55b49031a702caa2c6:20fdb8b37c354c05b9c5c6ae1807c4a7@sentry.platform.vn/11"
    )

    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "Wrong command"
        print "Format: python {} [file-log]".format(sys.argv[0])
        exit()

    try:
        file_name = sys.argv[1]
        pyg = Pygtail(file_name)
        first_line = pyg.next()
        # get log format and log type
        log_type, log_format = parser.detect_log_type(first_line)

        for line in Pygtail(file_name):
            error_info = parser.parse_log(line, log_type, log_format)
            status_code = error_info['status_code']

            if status_code == 200 or status_code == 404:
                client.capture(
                    "raven.events.Message",
                    message=log_type + " " + str(status_code),
                    extra=error_info,
                    # date=error_info['time']
                )

    except StopIteration:
        print "Nothing else to read"
    except Exception, e:
        client.captureException()
