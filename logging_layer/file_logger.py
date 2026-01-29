import json
from datetime import datetime

class FileLogger:
    def log(self, service, error, circuit_state):
        entry = {
            "time": datetime.utcnow().isoformat(),
            "service": service,
            "error": error,
            "circuit": circuit_state
        }
        with open("logs.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
