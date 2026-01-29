# 🤖 AI Call Agent – Error Recovery & Resilience System

## Overview

This project implements a **production-style error recovery and resilience system** for an AI Call Agent that depends on external services such as **ElevenLabs**, **LLM providers**, and **CRMs**.

The system is designed to handle failures gracefully by:
- Detecting errors
- Retrying transient failures
- Preventing cascading outages
- Alerting humans when needed
- Automatically recovering when services become healthy again

---

## Architecture

The system is structured as a **background worker** that processes calls from a queue and wraps all external service calls with a **resilience layer**.

### Key Components

- **Resilient Service Wrapper**
  - Retry logic with exponential backoff
  - Circuit breaker implementation
  - Integrated logging and alerting

- **Health Checker**
  - Periodic service health checks
  - Automatic circuit breaker reset on recovery

- **Logging Layer**
  - Structured local JSON file logging
  - Google Sheets logging (mocked)

- **Alert Manager**
  - Email alerts (mocked)
  - Telegram alerts (mocked)
  - Webhook alerts (mocked)

Each external dependency is isolated so failures do **not** impact the entire system.

---

## Error Categorization

A custom exception hierarchy is used to distinguish between:

### Transient Errors (Retried)
- Service unavailable (`503`)
- Timeouts
- Network failures

### Permanent Errors (Not Retried)
- Authentication failures (`401`)
- Invalid payloads
- Quota exceeded

---

## Retry Strategy

- Configurable retry policy
- Exponential backoff
- Default configuration:
  - Initial delay: **5 seconds**
  - Maximum retries: **3**
  - Backoff factor: **2**

Retries are applied **only** to transient errors.

---

## Circuit Breaker Pattern

Each external service has its own circuit breaker with three states:

- **CLOSED** – Normal operation
- **OPEN** – Fail-fast mode to prevent cascading failures
- **HALF_OPEN** – Recovery testing state

The circuit breaker opens after repeated failures and automatically resets when the service becomes healthy again.

---

## Health Checks & Recovery

Health checks run periodically in the background and:

- Monitor service availability
- Update service health state
- Reset circuit breakers when services recover

This enables **automatic self-healing** without manual intervention.

---

## Logging & Observability

All failures and system events are logged with:

- Timestamp
- Service name
- Error message
- Circuit breaker state

Logs are written to:
- Local structured JSON log files
- Google Sheets (mocked for demonstration)

---

## Alerting

Alerts are triggered when:
- A circuit breaker opens
- A call permanently fails

Alert channels:
- Email (mock)
- Telegram (mock)
- Webhook (mock)

---

## Graceful Degradation

When a service becomes unavailable:

- The current call is marked as failed
- The system continues processing the next contact
- No global blocking or crashes occur

---

## Required Scenario: ElevenLabs `503` Failure

The system correctly handles the required failure scenario:

1. ElevenLabs returns `503 Service Unavailable`
2. Error is classified as **transient**
3. Retries are attempted with exponential backoff:
   - 5s → 10s → 20s
4. After retries fail:
   - Call is marked as failed
   - Alerts are triggered
   - Circuit breaker opens
5. Health checks continue running
6. Once ElevenLabs becomes healthy:
   - Circuit breaker resets automatically
   - Call processing resumes

---

## How to Run

```bash
python main.py
```
