from core.exceptions import ServiceUnavailable

class FakeElevenLabs:
    def __init__(self):
        self.fail = True

    def synthesize(self):
        if self.fail:
            raise ServiceUnavailable("503 Service Unavailable")
        return "🔊 Audio generated successfully"

    def health_check(self):
        return not self.fail
