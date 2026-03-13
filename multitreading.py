import time
import threading

exit_event = threading.Event()

def task(name, delay):
    while True:
        time.sleep(delay)
        print("%s:%s"%(name,time.time()))
        if exit_event.is_set():
            break

t1 = threading.Thread(target=task,args=("fast-thread",1))
t2 = threading.Thread(target=task,args=("slow-thread",5))

t1.start()
t2.start()
n=0

try:
    while True:
        n+=1
        print("Main")
        time.sleep(1)
except KeyboardInterrupt:
    exit_event.set()