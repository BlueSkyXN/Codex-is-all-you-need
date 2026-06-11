---
name: performance-diagnosis
description: Use for diagnosing slow code, APIs, queries, memory growth, frontend load, build regressions, resource bottlenecks, and scalability limits.
---

# Performance diagnosis workflow

Use this workflow when there is a measurable performance problem or performance-sensitive change.

## Steps

1. Define the metric.
   - Latency
   - Throughput
   - Memory
   - CPU
   - I/O
   - Query time
   - Bundle size
   - Build time

2. Establish a baseline.
   - Use comparable commands, traces, profiler output, query plans, browser metrics, or logs.
   - Record environment and input size.

3. Form hypotheses.
   - Algorithm or data structure
   - Database/index/query
   - Network/API chatter
   - Cache behavior
   - Rendering or bundle cost
   - Build/tooling overhead
   - Memory leak or object retention

4. Test one change at a time.
   - Keep correctness tests in place.
   - Measure before/after.
   - Prefer targeted fixes over architecture replacement.

5. Confirm no regression.
   - Run relevant correctness checks.
   - Check edge cases and resource limits.
   - State noise or uncertainty in the measurement.

## Output

Return:

1. Metric and baseline
2. Bottleneck evidence
3. Change or recommendation
4. Before/after result
5. Remaining uncertainty

## Do not

- Do not claim speedups without measurement.
- Do not optimize code that is not on the measured path.
- Do not trade correctness, security, or data integrity for speed.
