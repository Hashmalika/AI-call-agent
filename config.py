RETRY_CONFIG = {
    "max_attempts": 3,
    "initial_delay": 5,
    "backoff_factor": 2
}

CIRCUIT_CONFIG = {
    "failure_threshold": 2,
    "recovery_timeout": 20
}

HEALTH_CHECK_INTERVAL = 10
