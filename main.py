import sys
import parser
import raven
import resume


RESUME = 0


if __name__ == '__main__':
    # initialize connection to sentry server
    client = raven.Client(
        dsn="http://ea8723b06f824d55b49031a702caa2c6:20fdb8b37c354c05b9c5c6ae1807c4a7@sentry.platform.vn/11"
    )

    if len(sys.argv) < 2:
        print "Wrong command"
        print "Format: python {} [option] [file-log]".format(sys.argv[0])
        exit("option\n -r : Resume")

    file_name = sys.argv[1]

    if len(sys.argv) == 3:
        RESUME = 1


    with open(file_name, "r") as f:
        # Resume
        if RESUME:
            f.seek(resume.get_last_location(file_name))
        log_format = ""
        for line in f:
            try:
                if not log_format:
                    log_type, log_format = parser.detect_log_type(line)
                    if log_type == 'HAPROXY2':
                        log_type = 'HAPROXY'
                error_info = parser.parse_log(line, log_type, log_format)
                status_code = error_info['status_code']

                if status_code == 502 or status_code == 503:
                    client.capture(
                        "raven.events.Message",
                        message=log_type + " " + str(status_code),
                        extra=error_info
                    )

            except Exception, e:
                client.captureException()

        # Save cached
        resume.save_to_cached(file_name, f.tell())
