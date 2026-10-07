# Observability

Monitoring tells you **that** something is wrong (CPU is at 95%, a pod is
down). Observability is being able to figure out **why**, from the data the
system already gives out, without adding new debug code every time.

## The three pillars

### Metrics

Numbers measured over time. For example CPU usage, memory, requests per
second, error rate, number of running pods.

- Cheap to store, good for dashboards and alerts
- Tell you something changed, but not much about one specific request
- Example: `container_cpu_usage_seconds_total` in Prometheus

### Logs

Text lines the app or system writes when something happens.

```text
2026-10-07 14:41:03 ERROR could not connect to database: timeout
```

- Give the details of what happened at one moment
- Can get huge and expensive to keep
- Much easier to search when they're structured (JSON) instead of plain text
- Example: `kubectl logs <pod>`

### Traces

One trace follows a single request through every service it touches, with
how long each step took.

```text
GET /checkout              420ms
├── auth-service            30ms
├── cart-service            50ms
└── payment-service        330ms   <- this is the slow part
```

- Most useful with microservices, where one request goes through many apps
- Need the app to be instrumented (usually with OpenTelemetry)

### How they fit together

An alert fires on a **metric** (error rate went up). The **trace** shows which
service the failing requests are slow or failing in. The **logs** of that
service show the actual error.

## Why observability is needed

- With many pods and services, you can't SSH into each one and look around
- Pods get deleted and replaced, so their local logs are gone with them
- Problems often only show up when several services talk to each other
- It's how you find the cause quickly instead of guessing, which keeps
  downtime short

## Common tools

| Pillar | Tools |
|---|---|
| Metrics | Prometheus, Grafana, Datadog, CloudWatch |
| Logs | Loki, ELK (Elasticsearch, Logstash, Kibana), Fluent Bit, CloudWatch Logs |
| Traces | Jaeger, Tempo, Zipkin, OpenTelemetry (for collecting) |
| Alerts | Alertmanager, Grafana alerting, PagerDuty |

## Kubernetes observability

What I'd look at in a Kubernetes cluster:

- **Cluster and nodes:** CPU, memory, disk per node
  (node-exporter, `kubectl top nodes`)
- **Pods and containers:** CPU, memory, restarts, OOMKilled
  (cAdvisor, `kubectl top pods`)
- **Kubernetes objects:** is the Deployment at the desired replicas, are
  pods stuck Pending or in ImagePullBackOff (kube-state-metrics)
- **Events:** `kubectl get events` shows scheduling failures, image pull
  errors, probe failures
- **App health:** readiness and liveness probes, plus `/health` endpoints
- **Logs:** `kubectl logs`, or shipped to Loki/ELK so they survive pod
  restarts

`kube-prometheus-stack`, which I used in this session, bundles most of
this: Prometheus, Alertmanager, Grafana, node-exporter and
kube-state-metrics, with ready-made dashboards and alert rules.
