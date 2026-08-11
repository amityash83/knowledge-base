---
title: kubectl
type: tool
domain: [devops]
status: stable
tags: [kubernetes, kubectl, operations]
sources: [raw-sources/archive/kubernetes-kubectl-common-commands.md]
created: 2026-08-11
updated: 2026-08-11
---

# kubectl

## Summary
The Kubernetes CLI for cluster inspection, debugging, and workload visibility. This page holds the ready-to-copy commands; concepts behind them live in [[kubernetes-cluster-fundamentals]].

## Details

### Cluster & workload inspection
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
```

### Troubleshooting a specific workload
```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

### Networking inspection
```bash
kubectl get svc -A
kubectl get ingress -A
kubectl describe svc <service-name>
```

### Recommended troubleshooting order
1. Inspect cluster and node health.
2. Narrow to the failing namespace or workload.
3. Read events, pod status, and logs.
4. Use `exec` only when direct container inspection is actually needed — it's the most invasive option.

## Open questions
- None; this is a stable command reference, expected to grow as new commands prove useful.

## Related
- [[kubernetes-cluster-fundamentals]]
- [[kubernetes-service-networking]]
