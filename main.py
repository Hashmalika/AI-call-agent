import time
from config import *
from core.retry import RetryPolicy
from core.circuit_breaker import CircuitBreaker
from core.health_check import HealthChecker
from core.resilience import ResilientService
from services.elevenlabs import FakeElevenLabs
from logging_layer.file_logger import FileLogger
from logging_layer.sheets_logger import SheetsLogger
from alerts.alert_manager import AlertManager
from core.exceptions import ServiceError

# Setup service
elevenlabs = FakeElevenLabs()

retry_policy = RetryPolicy(**RETRY_CONFIG)
circuit = CircuitBreaker(**CIRCUIT_CONFIG)

file_logger = FileLogger()
sheets_logger = SheetsLogger()

class CombinedLogger:
    def log(self, *args):
        file_logger.log(*args)
        sheets_logger.log(*args)

alert_manager = AlertManager()

resilient_eleven = ResilientService(
    "ElevenLabs",
    elevenlabs,
    retry_policy,
    circuit,
    CombinedLogger(),
    alert_manager
)

# Health checker
health = HealthChecker(HEALTH_CHECK_INTERVAL)
health.register("ElevenLabs", elevenlabs.health_check, circuit)
health.start()

# Call queue
queue = ["Pooja", "Nishita", "Aparana"]

print("\n Starting call processing...\n")

for person in queue:
    print(f"📞 Calling {person}")
    try:
        result = resilient_eleven.call(elevenlabs.synthesize)
        print("✅ Success:", result)
    except ServiceError:
        print("❌ Call failed, moving to next contact")

# Simulate recovery
print("\n Simulating ElevenLabs recovery in 25 seconds...\n")
time.sleep(25)
elevenlabs.fail = False

print("\n🔁 Retrying calls after recovery...\n")

for person in queue:
    print(f"📞 Calling {person}")
    try:
        result = resilient_eleven.call(elevenlabs.synthesize)
        print("✅ Success:", result)
    except:
        print("❌ Still failing")
