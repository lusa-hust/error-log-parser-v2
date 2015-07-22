import os
import os.path


def check_cached(file_name):
    cached_name = ".cached/" + file_name
    if os.path.isfile(cached_name):
        return True
    else:
        return False


def save_to_cached(file_name, location_in_byte):
    cached_name = ".cached/" + file_name
    if check_cached(file_name):
        os.remove(cached_name)
    f = open(cached_name, "w")
    f.write(str(location_in_byte))
    f.close()


def get_last_location(file_name):
    cached_name = ".cached/" + file_name
    if check_cached(file_name):
        f = open(cached_name, "r")
        old_size = int(f.read())
        new_size = os.stat(file_name).st_size
        if old_size > new_size:
            return 0
        f.close()
        return old_size
    return 0
