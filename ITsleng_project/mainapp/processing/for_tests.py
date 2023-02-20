import logging
import os
import time
from pprint import pprint

time_1d_ago = 1 * 24 * 60 * 60
time_2m_ago = 2 * 60


def remove_old_files(time_ago):
    time_now = time.time()
    target_path = os.path.join(os.getcwd(), 'sessionfiles')
    
    content = os.listdir(target_path)

    for file in content:
        file_path = os.path.join(target_path, file)
        time_cr = os.stat(file_path).st_ctime
        if (time_now - time_cr) > time_ago:
            os.remove(file_path)
            print(f'File: "{file}" deleted')