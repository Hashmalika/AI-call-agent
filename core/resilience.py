from core.retry import execute_with_retry
from core.exceptions import ServiceUnavailable

class ResilientService:
    def __init__(self, name, client, retry_policy, circuit_breaker, logger, alert_manager):
        self.name = name
        self.client = client
        self.retry_policy = retry_policy
        self.circuit_breaker = circuit_breaker
        self.logger = logger
        self.alert_manager = alert_manager

    def call(self, func):
        if self.circuit_breaker.is_open():
            raise ServiceUnavailable("Circuit breaker is OPEN")

        try:
            result = execute_with_retry(func, self.retry_policy)
            self.circuit_breaker.on_success()
            return result

        except Exception as e:
            self.circuit_breaker.on_failure()

            self.logger.log(self.name, str(e), self.circuit_breaker.status())

            if self.circuit_breaker.status() == "OPEN":
                self.alert_manager.alert(f"🚨 Circuit opened for {self.name}")

            raise
