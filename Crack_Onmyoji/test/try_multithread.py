import queue
import threading
import time
import random

q = queue.Queue()
threads = []


class MyThread(threading.Thread):
    def __init__(self, message_queue, thread_id, sleep_time):
        super(MyThread, self).__init__()
        self.message_queue = message_queue
        self.thread_id = thread_id
        self.sleep_time = sleep_time

    def run(self):
        time.sleep(self.sleep_time)
        self.message_queue.put(
            "I'm %d thread, slept %d seconds, and current time is %s" % (self.thread_id, self.sleep_time, time.ctime()))


for i in range(10):
    sleep_time = random.randint(1, 5)
    threads.append(MyThread(q, i, sleep_time))

for thread in threads:
    thread.start()

print("time to start multi-threading %s" % time.ctime())

count = 0
while True:
    if not q.empty():
        print(q.get())
        count += 1
    if count == 10:
        break
