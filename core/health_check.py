import threading
import time

class HealthChecker:
    def __init__(self, interval):
        self.services = {}
        self.interval = interval

    def register(self, name, check_func, circuit_breaker):
        self.services[name] = (check_func, circuit_breaker)

    def start(self):
        def loop():
            while True:
                for name, (check, breaker) in self.services.items():
                    try:
                        if check():
                            breaker.on_success()
                            print(f"[HEALTH] {name} is healthy")
                    except:
                        pass
                time.sleep(self.interval)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
