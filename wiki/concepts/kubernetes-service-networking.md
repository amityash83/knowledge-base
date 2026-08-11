---
title: Kubernetes Service Networking
type: concept
domain: [devops]
status: stable
tags: [networking, kubernetes, ingress, services]
sources: [raw-sources/archive/networking-service-routing-basics.md]
created: 2026-08-11
updated: 2026-08-11
---

# Kubernetes Service Networking

## Summary
Services provide stable virtual endpoints for dynamic, ephemeral workloads. Ingress and gateway layers manage north-south traffic into a cluster, while DNS, load balancers, and service discovery form the path connecting external clients to internal workloads.

## Details

### Traffic path
1. A client resolves a DNS name to a reachable endpoint.
2. Traffic reaches a load balancer, ingress controller, or gateway.
3. Routing rules send traffic to a Service.
4. The Service forwards requests to healthy backend pods.

### Inspection commands
```bash
kubectl get svc -A
kubectl get ingress -A
kubectl describe svc <service-name>
```

## Open questions
- None outstanding; stable reference note.

## Related
- [[kubernetes-cluster-fundamentals]]
- [[terraform-workflow]]
