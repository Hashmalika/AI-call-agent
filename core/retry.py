import time
from core.exceptions import TransientServiceError

class RetryPolicy:
    def __init__(self, max_attempts, initial_delay, backoff_factor):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor

def execute_with_retry(func, retry_policy):
    attempt = 0
    delay = retry_policy.initial_delay

    while True:
        try:
            return func()
        except TransientServiceError:
            attempt += 1
            if attempt >= retry_policy.max_attempts:
                raise
            print(f"[RETRY] Attempt {attempt} failed. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= retry_policy.backoff_factor
