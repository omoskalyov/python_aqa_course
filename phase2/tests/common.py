
import datetime


def get_time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ('.%03d' % (datetime.datetime.now().microsecond / 1000))
