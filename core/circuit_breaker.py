import time

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def is_open(self):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("[CIRCUIT] Moving to HALF_OPEN state")
                self.state = "HALF_OPEN"
                return False
            return True
        return False

    def on_success(self):
        if self.state != "CLOSED":
            print("[CIRCUIT] Reset to CLOSED")
        self.failures = 0
        self.state = "CLOSED"

    def on_failure(self):
        self.failures += 1
        if self.failures >= self.failure_threshold:
            if self.state != "OPEN":
                print("[CIRCUIT] OPENED due to failures")
            self.state = "OPEN"
            self.last_failure_time = time.time()

    def status(self):
        return self.state
