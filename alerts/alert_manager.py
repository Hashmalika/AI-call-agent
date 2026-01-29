class AlertManager:
    def alert(self, message):
        print(f"[EMAIL] {message}")
        print(f"[TELEGRAM] {message}")
        print(f"[WEBHOOK] {message}")
