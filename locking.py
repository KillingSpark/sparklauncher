import os

LOCK_PATH = os.path.expanduser("~")+"/.config/sparklauncher/.sparklauncherlock"
LOCK_DIR = os.path.expanduser("~")+"/.config/sparklauncher"

def check_lock_file():
    if not os.path.exists(LOCK_DIR):
        os.mkdir(LOCK_DIR)
    return os.path.exists(LOCK_PATH)

def create_lock_file():
    os.open(LOCK_PATH, os.O_CREAT)

def delete_lock_file():
    os.remove(LOCK_PATH)