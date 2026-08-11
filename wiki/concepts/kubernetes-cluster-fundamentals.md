---
title: Kubernetes Cluster Fundamentals
type: concept
domain: [devops]
status: stable
tags: [kubernetes, containers, orchestration]
sources: [raw-sources/archive/kubernetes-cluster-fundamentals.md, raw-sources/archive/kubernetes-kubectl-common-commands.md]
created: 2026-08-11
updated: 2026-08-11
---

# Kubernetes Cluster Fundamentals

## Summary
A Kubernetes cluster is split into a control plane (manages cluster state) and worker nodes (run workloads). Kubernetes favors declarative desired state over imperative host management — you describe what you want, and controllers continuously reconcile actual state toward it.

## Details

### Control plane
Manages cluster state through the API server, scheduler, and controllers.

### Worker nodes
Run pods and rely on kubelet, the container runtime, and kube-proxy.

### Request-to-running flow
1. A user submits a manifest to the API server.
2. The scheduler assigns pods to suitable nodes.
3. Controllers reconcile actual state toward desired state.
4. Kubelet ensures containers are running on the assigned node.
5. Services and networking provide stable connectivity to workloads (see [[kubernetes-service-networking]]).

### Everyday inspection commands
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
```

### Troubleshooting commands
```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

Recommended troubleshooting order: inspect cluster/node health → narrow to the failing namespace or workload → read events, pod status, and logs → only use `exec` when direct container inspection is actually needed.

## Open questions
- None outstanding from the source notes; this page is a stable reference.

## Related
- [[kubernetes-service-networking]]
- [[terraform-workflow]]
- [[devops-lab-platform-foundation]]
- [[aiops]]
