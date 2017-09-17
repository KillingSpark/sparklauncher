import os
import fcntl

LOCK_FD = os.open("/tmp/.sparklauncherlock", os.O_CREAT | os.O_RDWR)

def check_lock_file():
    try:
        fcntl.lockf(LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError, exception:
        print("ERROR" + exception.message)
        return True
    return False