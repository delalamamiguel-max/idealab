# Constitution: Pub/Sub Load Testing

## Purpose
Ensure the Pub/Sub system can handle expected and peak loads reliably, with minimal latency and no message loss. This agent governs the design, execution, and analysis of load testing scenarios.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ No unmonitored message loss  
✘ No unbounded latency under load  
✘ No untested failure recovery scenarios  
✘ No load tests without metrics collection  
✘ No production deployment without load test validation
✘ No anonymous consumer groups or default-thread settings—every scenario must define explicit consumer group IDs, partition/thread mappings, and offset reset policies.
✘ Never assume internet access, specific DNS, or direct registry access
✘ **No silent failures** - All dependency checks, network validation, and prerequisite verification must fail loudly with actionable error messages
✘ **No undocumented dependencies** - All libraries, versions, and system requirements must be explicit
✘ **No port conflicts** - Metrics servers and services must check for port availability

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Simulate realistic producer/consumer concurrency  
✔ Use load testing tools (e.g., JMeter, Gatling, Locust, custom Java clients)  
✔ Measure throughput, latency, error rate, resource usage, consumer lag, and backlog drain time per consumer group  
✔ Test with varying message sizes and burst patterns  
✔ Include failure scenarios (e.g., broker crash, slow consumer)  
✔ Collect metrics via Prometheus, Grafana, or logs  
✔ Document producer configuration (ack level, batch size, linger, compression) and consumer configuration (max poll interval, fetch size, thread count) for each test.  
✔ Provide a capacity matrix that maps partitions to consumer group threads and highlights saturation or rebalancing events.
✔ Implement retry logic with exponential backoff for transient failures

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Use containerized test environments for reproducibility  
➜ Automate load tests in CI/CD pipelines  
➜ Visualize results with dashboards  
➜ Compare results against SLA thresholds  
➜ Document test scenarios and outcomes for audits  
➜ Include soak tests and spike tests
➜ Stress-test rebalancing by varying consumer group membership and thread counts mid-run to validate recovery time.

---

### IV. Sample Load Test Setup

#### Tools
- **Apache JMeter**: For HTTP-based Pub/Sub APIs
- **Gatling**: For high-performance simulation
- **Kafka Performance Tool**: If using Kafka (`kafka-producer-perf-test.sh`)
- **Custom Java Clients**: Using `ExecutorService` for parallelism

#### Metrics to Track
- Message throughput (msg/sec)
- End-to-end latency
- Consumer lag (group and partition level)
- CPU/memory
- Producer retry/error counts
- Consumer thread utilization and poll duration percentiles

---

**Version**: 1.1.0  
**Last Updated**: 2025-10-27
