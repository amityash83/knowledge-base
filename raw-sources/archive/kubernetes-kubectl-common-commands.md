---
title: Kubernetes Kubectl Common Commands
tags: [kubernetes, kubectl, snippets, operations]
domain: kubernetes
difficulty: beginner
created: 2026-04-09
updated: 2026-04-09
---

# Kubernetes Kubectl Common Commands

## Summary
This snippet note collects frequently used `kubectl` commands for cluster inspection, debugging, and workload visibility. It is meant to be copied quickly during troubleshooting or learning sessions.

## Concepts
- Snippet notes should hold reusable operational commands with enough context to avoid misuse.
- Grouping commands by intent improves scan speed during incidents.
- Snippets complement knowledge notes rather than replacing them.

## Commands / Code
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

## Architecture / Flow
1. Inspect cluster and node health.
2. Narrow the failing namespace or workload.
3. Read events, pod status, and logs.
4. Use `exec` only when direct container inspection is needed.

## Use Cases
- Day-to-day Kubernetes operations.
- Quick troubleshooting during deployments.
- Learning the command patterns behind cluster diagnostics.

## Related Topics
- [[kubernetes-cluster-fundamentals]]
- [[networking-service-routing-basics]]
- [[devops-lab-platform-foundation]]

## Tags
#kubernetes #kubectl #snippets #operations
