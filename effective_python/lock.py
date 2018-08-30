from threading import Lock, Thread


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


def run_threader(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


if __name__ == '__main__':
    how_many = 10 ** 5
    counter = LockingCounter()
    run_threader(worker, how_many, counter)
    print('Counter should be %d,found %d' % (5 * how_many, counter.count))
