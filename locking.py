import os

def check_lock_file():
    return os.path.exists(os.path.expanduser("~")+"/.sparklauncherlock")

def create_lock_file():
    os.open(os.path.expanduser("~")+"/.sparklauncherlock", os.O_CREAT)

def delete_lock_file():
    os.remove(os.path.expanduser("~")+"/.sparklauncherlock")