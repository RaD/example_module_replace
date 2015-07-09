import threading
import time

SLEEP = 4
TICK = 0.1


class ThreadTaskA(threading.Thread):
    name = 'Task A'
    counter = 0

    def __init__(self, event):
        super(ThreadTaskA, self).__init__()
        self.event = event

    def run(self):
        print('thread {} started'.format(self.name))
        while not self.event.is_set():
            time.sleep(TICK)
            self.counter -= TICK
            if self.counter < 0.:
                self.counter = SLEEP
                print('{} tick'.format(self.name))
        print('thread {} finished'.format(self.name))
