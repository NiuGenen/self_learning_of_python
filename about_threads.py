import threading
from time import ctime,sleep

def th1(num):
    for i in range(0,10):
        print(i * num)
        sleep(1)

th = threading.Thread(target=th1, args=1)
th.setDaemon(True)
th.start()