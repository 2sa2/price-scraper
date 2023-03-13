import os
from datetime import datetime

# defines location to store previous price sheets
location = ''
def change_name(file):
    os.rename(file, location + datetime.fromtimestamp(os.stat(file).st_mtime).strftime('%Y-%m-%d') + '.ods')
