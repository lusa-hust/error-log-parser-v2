__author__ = 'li'

import sys
import parser
import raven


if __name__ == '__main__':
    # initialize connection to sentry server
    client = raven.Client(
        dsn="http://ea8723b06f824d55b49031a702caa2c6:20fdb8b37c354c05b9c5c6ae1807c4a7@sentry.platform.vn/11"
    )

    try:
        if len(sys.argv) is not 2:
            raise "Wrong command"
    except Exception:
        client.captureException()

    with open(sys.argv[1], "r") as f:
        for line in f:
            try:
                error_info = parser.parse_log(line)
                status_code = error_info['status_code']
                if status_code == '200' or status_code == '404':
                    client.capture(
                        "raven.events.Message",
                        message=status_code,
                        extra=error_info
                    )
            except Exception, e:
                client.captureException()