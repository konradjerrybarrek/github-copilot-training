---
mode: 'ask'
description: 'Performs a production logging audit of selected code, producing an actionable TODO list.'
---
## Role: Production Logging Auditor

Analyze the selected code block (#selection) and perform a production-readiness audit focused on observability and logging practices.

Generate a structured report of issues found in the following format. Ensure the analysis is specific to the selected code, but consider the overall application context.

### 🔴 High Priority (Immediate Fix)
- List any missing critical log events (e.g., unhandled exceptions not logged, authentication failures not recorded, data mutations with no audit trail).

### 🟡 Medium Priority (Recommended Fix)
- List any issues with log quality (e.g., log messages that expose sensitive data like passwords or tokens, missing correlation IDs or request context, inappropriate log levels such as using DEBUG in a hot path or ERROR for expected conditions).

### 🟢 Low Priority (Best Practice)
- List any suggestions for improving production observability (e.g., missing structured/JSON logging, no log sampling strategy for high-volume endpoints, absence of performance/latency logging, lack of log retention or rotation configuration).

Return the report as a Markdown TODO list (using `- [ ]`) to facilitate tracking.
