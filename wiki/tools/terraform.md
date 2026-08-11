---
title: Terraform CLI
type: tool
domain: [devops]
status: stable
tags: [terraform, cli, iac]
sources: [raw-sources/archive/terraform-terraform-cli-workflow.md]
created: 2026-08-11
updated: 2026-08-11
---

# Terraform CLI

## Summary
The Terraform command-line workflow used to format, initialize, validate, plan, and apply infrastructure changes in a controlled, reviewable way. The reasoning behind each step lives in [[terraform-workflow]].

## Details

### Standard sequence
```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform show
```

1. Normalize formatting.
2. Initialize the working directory and providers.
3. Validate configuration quality.
4. Generate and review a plan file.
5. Apply only the approved, saved plan — never re-plan implicitly at apply time.
6. Inspect applied state with `show`.

## Open questions
- None; stable command reference.

## Related
- [[terraform-workflow]]
- [[devops-lab-platform-foundation]]
