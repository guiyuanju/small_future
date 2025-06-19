import time

class EventLoop:
    def __init__(self):
        self.event_loop = []

    def after(self, secs, f):
        self.event_loop.append((time.time()+secs, f)) 

    def run(self):
        self.start_time = time.time()
        while True:
            if len(self.event_loop) > 0:
                t, f = self.event_loop.pop()
                if time.time() >= t:
                    f()
                else:
                    self.event_loop.insert(0, (t, f))
            else:
                return
            
EVENT_LOOP = EventLoop()

class Future:
    def __init__(self, future):
        self.thens = []
        # using async timer to simulate aysnc behavior
        EVENT_LOOP.after(future, lambda: [f() for f in self.thens])

    def then(self, f):
        self.thens.append(f)


def async_write(_):
    # simulate need 3 seconds to finish writing
    # can use epoll for an actual implementation
    return 3

def main():
    Future(async_write("some writing task")) \
        .then(lambda: (print("writing task done")))
    EVENT_LOOP.after(2, lambda: print(2))
    EVENT_LOOP.after(1, lambda: print(1))
    EVENT_LOOP.after(5, lambda: print(5))
    EVENT_LOOP.run()

if __name__ == "__main__":
    main()