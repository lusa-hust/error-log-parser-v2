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
        file_name = sys.argv[2]
        if sys.argv[1] == '-r':
            RESUME = 1
        else:
            exit("Unknown Option")

    with open(file_name, "r") as f:
        log_type, log_format = parser.detect_log_type(f.readline())
        if log_type == 'HAPROXY2':
            log_type = 'HAPROXY'

        if RESUME:
            f.seek(resume.get_last_location(file_name))
        else:
            f.seek(0)

        for line in f:
            try:
                error_info = parser.parse_log(line, log_type, log_format)
                status_code = error_info['status_code']

                if status_code == 200 or status_code == 404:
                    client.capture(
                        "raven.events.Message",
                        message=log_type + " " + str(status_code),
                        extra=error_info,
                        date=error_info['time']
                    )

            except Exception, e:
                client.captureException()

        # Save cached
        resume.save_to_cached(file_name, f.tell())
