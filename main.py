import sys
import parser
import raven
import resume
import os
import commands


RESUME = 0


def gather_log_errors(file_name, last_position, sentry_client):
    print "reading file {}".format(file_name)
    with open(file_name, "r") as f:
        log_type, log_format = parser.detect_log_type(f.readline())

        if log_type == 'HAPROXY2':
            log_type = 'HAPROXY'

        f.seek(last_position)

        for line in f:
            try:
                error_info = parser.parse_log(line, log_type, log_format)
                status_code = error_info['status_code']

                if status_code == 200 or status_code == 404:
                    sentry_client.capture(
                        "raven.events.Message",
                        message=log_type + " " + str(status_code),
                        extra=error_info,
                        # date=error_info['time']
                    )

            except Exception, e:
                client.captureException()

        # Save cached
        if file_name.find('1') == -1:
            # if the file is not logrotated file, containing no '1' in the file name
            # then save it to cached
            resume.save_to_cached(file_name, f.tell())


def get_last_log_file(file_name):
    output = commands.getoutput('find -type f -name "{}*" | sort -r'.format(file_name))
    files = output.split('\n')
    return len(files), files[0]

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

    if not resume.os.path.exists(".cached"):
        resume.os.makedirs(".cached")

    if RESUME:
        last_position = resume.get_last_location(file_name)
        file_size = os.path.getsize(file_name)

        if last_position < file_size:
            num_file, last_log = get_last_log_file(file_name)
            if num_file == 1:
                # file haven't been rotated
                gather_log_errors(file_name, last_position, client)
            else:
                # case: log will be written to logname.1
                # read the previous log
                gather_log_errors(file_name, last_position, client)
                # read the current log
                gather_log_errors(last_log, 0, client)
        elif last_position > file_size:
            # file log is rotated
            num_file, last_log = get_last_log_file(file_name)
            if num_file == 1:
                # there is only 1 log file
                # case: content is erased
                gather_log_errors(file_name, 0, client)
            else:
                # case: rotated log is renamed to logname.1
                # there are more than 1 log file
                # read the previous rotated log
                gather_log_errors(last_log, last_position, client)
                # read the current log
                gather_log_errors(file_name, 0, client)
    else:
        gather_log_errors(file_name, 0, client)
