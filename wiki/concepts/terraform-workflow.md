---
title: Terraform Infrastructure Workflow
type: concept
domain: [devops]
status: stable
tags: [terraform, infrastructure-as-code, devops]
sources: [raw-sources/archive/terraform-infrastructure-workflows.md, raw-sources/archive/terraform-terraform-cli-workflow.md]
created: 2026-08-11
updated: 2026-08-11
---

# Terraform Infrastructure Workflow

## Summary
Terraform manages infrastructure through declarative configuration and state comparison. `plan` previews drift and intended changes before `apply`; remote state and locking reduce team conflicts and accidental overwrites.

## Details

### Standard workflow
1. Define infrastructure resources in code.
2. Initialize providers and modules.
3. Validate syntax and dependency resolution.
4. Review the execution plan before applying changes.
5. Store state securely and monitor drift over time.

### CLI sequence
```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform show
```

Running with a saved plan file (`plan -out=tfplan` → `apply tfplan`) guarantees you apply exactly what you reviewed, not a plan re-computed at apply time.

## Open questions
- None outstanding; stable reference note.

## Related
- [[kubernetes-cluster-fundamentals]]
- [[devops-lab-platform-foundation]]
