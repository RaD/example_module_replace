import threading
import time

SLEEP = 3
TICK = 0.1


class ThreadTaskB(threading.Thread):
    name = 'Task B'
    counter = 0

    def __init__(self, event):
        super(ThreadTaskB, self).__init__()
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
