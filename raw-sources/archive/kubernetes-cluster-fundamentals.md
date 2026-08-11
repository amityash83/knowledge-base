---
title: Kubernetes Cluster Fundamentals
tags: [kubernetes, containers, orchestration]
domain: kubernetes
difficulty: intermediate
created: 2026-04-09
updated: 2026-04-09
---

# Kubernetes Cluster Fundamentals

## Summary
This note explains the core components of a Kubernetes cluster, including the control plane, worker nodes, and declarative workload management. It is designed as a durable reference for both learning and operational recall.

## Concepts
- The control plane manages cluster state through the API server, scheduler, and controllers.
- Worker nodes run pods and rely on kubelet, the container runtime, and kube-proxy.
- Kubernetes favors declarative desired state over imperative host management.

## Commands / Code
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A
```

## Architecture / Flow
1. A user submits a manifest to the API server.
2. The scheduler assigns pods to suitable nodes.
3. Controllers reconcile actual state toward desired state.
4. Kubelet ensures containers are running on the assigned node.
5. Services and networking provide stable connectivity to workloads.

## Use Cases
- Understanding how workloads are scheduled and maintained.
- Troubleshooting cluster state and node health.
- Building a mental model before studying ingress, storage, or observability.

## Related Topics
- [[networking-service-routing-basics]]
- [[kubernetes-kubectl-common-commands]]
- [[devops-lab-platform-foundation]]
- [[02-Knowledge/index|Knowledge Index]]

## Tags
#kubernetes #containers #orchestration #devops
