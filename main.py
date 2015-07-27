import sys
import parser
import os
from pygtail import Pygtail
import raven


def is_erased(file_name):
    inode = os.stat(file_name).st_ino
    file_size = os.stat(file_name).st_size
    saved_inode, saved_offset = get_offset_info(file_name)

    if(file_size < saved_offset) and (saved_inode == inode):
        return True
    else:
        return False


def get_offset_info(file_name):
    offset_file = file_name + '.offset'
    with open(offset_file, 'r') as f:
        inode = int(f.readline())  # read inode
        offset = int(f.readline())  # read offset
        return inode, offset


if __name__ == '__main__':
    # initialize connection to sentry server
    client = raven.Client(
        dsn="http://ea8723b06f824d55b49031a702caa2c6:20fdb8b37c354c05b9c5c6ae1807c4a7@sentry.platform.vn/11"
    )

    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "Wrong command"
        print "Format: python {} [file-log]".format(sys.argv[0])
        exit()

    file_name = sys.argv[1]

    if is_erased(file_name):
        # forget about saved offset
        # delete offset file
        # print "remove file"  # test point
        os.remove(file_name+'.offset')

    try:
        pyg = Pygtail(file_name)
        first_line = pyg.next()
        # get log format and log type
        log_type, log_format = parser.detect_log_type(first_line)

        for line in Pygtail(file_name):
            # print line  # test point
            error_info = parser.parse_log(line, log_type, log_format)
            status_code = error_info['status_code']

            if status_code == 502 or status_code == 503:
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
