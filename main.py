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
    def __init__(self, simulate_delays, future):
        self.thens = []
        def run():
            res = future()
            for f in self.thens:
                res = f(res)
            return res
        # using async timer to simulate aysnc behavior
        EVENT_LOOP.after(simulate_delays, run)

    def then(self, f):
        self.thens.append(f)
        return self

def async_write():
    # can use epoll for an actual implementation
    return lambda: "return value from async write"

def main():
    print("some random task 1")
    Future(3, async_write()) \
        .then(lambda _: (print("writing task done"))) \
        .then(lambda x: (print("previous result is " + str(x))))
    print("some random task 2")
    EVENT_LOOP.after(2, lambda: print("timer at 2 sec"))
    print("some random task 3")
    EVENT_LOOP.after(1, lambda: print("timer at 1 sec"))
    EVENT_LOOP.after(5, lambda: print("timer at 5 sec"))
    EVENT_LOOP.run()

if __name__ == "__main__":
    main()