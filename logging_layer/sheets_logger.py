class SheetsLogger:
    def log(self, service, error, circuit_state):
        print(f"[SHEETS] {service} | {error} | {circuit_state}")
